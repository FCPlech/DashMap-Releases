# Mirroring a release to the public

Releases are mirrored by hand, one tag at a time, with your own `gh auth`
(no tokens, no secrets, no automation):

```bash
# from this repo root (or anywhere: the script takes --private/--public):
./scripts/mirror_release.py v1.12.0

# preview only, then run for real:
./scripts/mirror_release.py v1.12.0 --dry-run
```

For the given tag the script reads title/notes/assets from the private
repo, downloads the assets to a temp dir, creates (or refreshes) the same
tag here, and prunes public releases beyond the newest 3. Private tags are
never touched: pruning is mirror-only.

Rules that keep the source closed:

- Only binary assets cross over. Never commit app source or build internals
  here: the automatic "Source code" zips GitHub attaches to every release
  are built from this repo's own git data, so whatever is committed here is
  what they contain.
- Drafts are refused. Publish (or pre-release) the tag privately first.
- The script needs `gh auth login` reaching both repos; nothing else.
