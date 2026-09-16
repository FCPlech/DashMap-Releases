# DashMap-Releases

<p align="center">
  <img src="branding/dashmap_logo.png" alt="DashMap logo" width="400" />
</p>

Public download point for **DashMap** releases. This repo contains **only
binaries** (see below): no source code, no build tooling. The app's own
in-app updater tracks this repo.

> DashMap itself is a closed-source, independent project. **Not affiliated
> with, endorsed by, or supported by Royal Enfield.** "Royal Enfield",
> "Himalayan" and "Tripper" are trademarks of their owners.

## What DashMap is

Low-power motorcycle navigation for the Royal Enfield Himalayan 450,
projected onto the bike's round Tripper TFT dash with the phone screen off.
Instead of mirroring the display, DashMap renders the map off-screen,
hardware-encodes it to H.264 and streams it over the bike's Wi-Fi, so the
phone stays cool and sips battery for the whole ride.

- **Navigation**: share a destination from Google Maps, preview the road
  route, send it to the dash. Turn-by-turn with automatic off-route
  rerouting, online routing first and an offline package when there is no
  signal. Online place search, planned multi-stop trips and imported GPX
  tracks included.
- **Offline maps**: full packages (Valhalla routing tiles and Nearby
  streets database) downloadable straight from the app, no computer
  needed. The visual map background streams online; Minimalist mode rides
  on the streets database with no tiles at all.
- **Dash control**: joystick zoom, saved routes and GPX lists on the dash,
  a media menu (next, seek, play/pause, artwork), and incoming calls with
  answer/reject from the dash.
- **Voice guidance**: off, chime-before-turns, or full spoken turn-by-turn,
  on-device, in PT-BR and English.
- **Rides**: every finished navigation saved automatically with distance,
  duration, speeds and a track map.
- **Private by design**: no account, no server. Everything lives on the
  device.

Requires a 64-bit ARM Android phone on Android 10+ and a Himalayan 450 with
the Tripper dash.

## The binaries

Every release carries up to three files:

- **`DashMap.apk`**: the app itself. Sideload it (allow "install unknown
  apps" when asked). Signed with the same key every time, so updates
  install in place and keep your data. Android may show an "unverified app"
  warning: expected for a self-managed community key.
- **`DashMapOfflineMaps-linux`**: the offline-maps desktop tool for
  Linux. Prepares routing + streets packages on a computer and sends them
  to the phone over USB or Wi-Fi. Optional: the app also downloads
  ready-made packages by itself.
- **`DashMapOfflineMaps-windows.exe`**: the same desktop tool for Windows.

## Credits

Same licenses and attributions the app carries under Settings → Credits,
license first:

- **NorthStar**: © 2026 Aditya Dasika · Apache License 2.0
- **OpenStreetMap contributors**: © OpenStreetMap contributors · ODbL, attribution required
- **OpenFreeMap**: map tiles · OSM data © contributors (ODbL)
- **MapLibre**: map rendering · BSD-2-Clause
- **Valhalla**: routing engine · MIT
- **OSRM**: online routing service · shared demo server, fair use
- **Overpass API**: live map queries · public instance, fair use
- **Nominatim**: place search · OSMF usage policy
- **Open-Meteo**: weather data · free API, see its terms (data CC-BY 4.0)
- **Geofabrik**: data extracts · OSM data (ODbL)
- **better-dash (Apache-2.0)**: dash protocol reference; implementation independent

The routing tiles and street databases in these releases derive from
OpenStreetMap data, so the ODbL credit above travels with them. See
https://osm.org/copyright.
