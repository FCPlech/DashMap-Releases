# DashMap-Releases

Public download point for **DashMap** releases (Android APK plus the
offline-maps desktop tool for Windows and Linux). The app's own in-app
updater and Obtainium track this repo.

> DashMap itself is a closed-source, independent project. **Not affiliated
> with, endorsed by, or supported by Royal Enfield.** "Royal Enfield",
> "Himalayan" and "Tripper" are trademarks of their owners.

## What lives here

- **GitHub Releases**: versioned `DashMap.apk` + `DashMapOfflineMaps-*`
  binaries, mirrored from the private development repo on purpose, whenever
  the author runs `./scripts/mirror_release.py <tag>`.
- **This git history**: only this README, `docs/` and `scripts/`. No app
  source, no build tooling internals.

## Install / update

Grab the latest APK from
[Releases](https://github.com/FCPlech/DashMap-Releases/releases/latest) and
sideload it (allow "install unknown apps" when asked). Every release is
signed with the same key, so updates install in place and keep your data:
rides, Garage and offline maps are preserved.

Android may show an "unverified app" warning: expected for a self-managed
community key.

## Credits

Map data © OpenStreetMap contributors (ODbL), map imagery via OpenFreeMap,
offline routing built with the Valhalla engine, forecasts by Open-Meteo.
Full licenses live in the app under Settings → Credits.
