#!/usr/bin/env python3
"""Mirror one private DashMap release to this public repo.

Manual use, whenever you want the public releases to catch up. Runs on your
machine with your own `gh auth login` (it must reach both repos): no tokens,
no secrets, no automation.

    ./scripts/mirror_release.py v1.12.0
    ./scripts/mirror_release.py v1.12.0 --dry-run
    ./scripts/mirror_release.py v1.12.0 --no-prune

For TAG, it:
  1. reads title/notes/asset names from the private release
  2. downloads its assets to a temp dir
  3. creates the public release if missing (same tag/title/notes), else
     refreshes title/notes and syncs assets (stale ones removed, current
     ones uploaded)
  4. prunes public releases beyond --keep newest (same policy as the app's
     own release workflow). Tags pruned here are mirror-only: the private
     repo is never deleted from, only read.

Only binary assets cross over. This repo's own git history (and the
automatic "Source code" zips GitHub attaches to every release) never sees
private source. Drafts are refused (publish or pre-release first).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_PRIVATE = "FCPlech/DashMap"
DEFAULT_PUBLIC = "FCPlech/DashMap-Releases"


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tag", help="release tag to mirror (e.g. v1.12.0)")
    ap.add_argument("--private", default=DEFAULT_PRIVATE, help="source repo (default: %(default)s)")
    ap.add_argument("--public", default=DEFAULT_PUBLIC, help="mirror repo (default: %(default)s)")
    ap.add_argument("--keep", type=int, default=3,
                    help="keep this many newest public releases, prune the rest (0 disables)")
    ap.add_argument("--no-prune", action="store_true", help="skip pruning")
    ap.add_argument("--dry-run", action="store_true", help="print what would happen, change nothing")
    args = ap.parse_args()

    who = gh("auth", "status")
    if who.returncode != 0:
        print("ERROR: gh is not logged in (run `gh auth login` first).", file=sys.stderr)
        return 1

    meta = gh("release", "view", args.tag, "--repo", args.private,
              "--json", "name,body,assets,isDraft")
    if meta.returncode != 0:
        print(f"ERROR: no release {args.tag} in {args.private}.", file=sys.stderr)
        return 1
    info = json.loads(meta.stdout)
    if info.get("isDraft"):
        print(f"ERROR: {args.tag} is a draft in {args.private}; publish it first.", file=sys.stderr)
        return 1
    title = info.get("name") or args.tag
    body = info.get("body") or ""
    assets = [a["name"] for a in info.get("assets", []) if a.get("name")]
    print(f"private {args.tag}: {len(assets)} assets, title {title!r}")

    if args.dry_run:
        print(f"would download: {', '.join(assets) or '(none)'}")
        print(f"would create-or-refresh public {args.tag} with same title/notes")
        if not args.no_prune and args.keep > 0:
            print(f"would prune public releases beyond newest {args.keep}")
        return 0

    tmp = Path(tempfile.mkdtemp(prefix="mirror-"))
    try:
        dl = gh("release", "download", args.tag, "--repo", args.private, "--dir", str(tmp))
        if dl.returncode != 0:
            print(f"ERROR: could not download assets of {args.tag}.", file=sys.stderr)
            return 1
        files = sorted(p for p in tmp.iterdir() if p.is_file())
        if [p.name for p in files] != sorted(assets):
            print("WARNING: downloaded set differs from the release asset list; "
                  "continuing with what landed in temp.", file=sys.stderr)

        notes_file = tmp / "notes.md"
        notes_file.write_text(body)
        exists = gh("release", "view", args.tag, "--repo", args.public,
                    "--json", "assets", "--jq", ".assets[].name")
        if exists.returncode != 0:
            print(f"creating public {args.tag} ...")
            create = subprocess.run(
                ["gh", "release", "create", args.tag, "--repo", args.public,
                 "--title", title, "--notes-file", str(notes_file),
                 *[str(p) for p in files]])
            if create.returncode != 0:
                print(f"ERROR: could not create public {args.tag}.", file=sys.stderr)
                return 1
        else:
            live = set(exists.stdout.split())
            want = {p.name for p in files}
            for stale in sorted(live - want):
                print(f"removing stale asset {stale} ...")
                if gh("release", "delete-asset", args.tag, stale,
                       "--repo", args.public, "--yes").returncode != 0:
                    print(f"ERROR: could not remove {stale}.", file=sys.stderr)
                    return 1
            print(f"uploading {len(files)} files to public {args.tag} ...")
            up = subprocess.run(
                ["gh", "release", "upload", args.tag, "--repo", args.public,
                 *[str(p) for p in files], "--clobber"])
            if up.returncode != 0:
                print(f"ERROR: upload to public {args.tag} failed.", file=sys.stderr)
                return 1
            if gh("release", "edit", args.tag, "--repo", args.public,
                   "--title", title, "--notes-file", str(notes_file)).returncode != 0:
                print(f"ERROR: could not refresh title/notes of public {args.tag}.",
                      file=sys.stderr)
                return 1

        if not args.no_prune and args.keep > 0:
            listed = gh("release", "list", "--repo", args.public, "--limit", "100",
                        "--json", "tagName,createdAt,isDraft",
                        "--jq", '[.[] | select(.isDraft | not)] | sort_by(.createdAt) | reverse')
            if listed.returncode == 0:
                try:
                    ordered = [r["tagName"] for r in json.loads(listed.stdout)]
                except (ValueError, KeyError):
                    ordered = []
                for old in ordered[args.keep:]:
                    print(f"pruning public {old} ...")
                    gh("release", "delete", old, "--repo", args.public,
                       "--yes", "--cleanup-tag")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"https://github.com/{args.public}/releases/tag/{args.tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
