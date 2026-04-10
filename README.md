# Subway Builder Maps

Custom maps for [Subway Builder](https://store.steampowered.com/app/3029480/Subway_Builder/) by ryandicicco. Cities the base game doesn't ship with; built, tuned, and kept up to date here.

## Available maps

<!-- MAPS_TABLE:START -->
| Code | City | Country | Version | Last updated |
| --- | --- | --- | --- | --- |
| AMS | Amsterdam | NL | 1.2.0 | 2026-03-16 |
| CAI | Cairo | EG | 2.2.0 | 2026-04-10 |
| GEG | Spokane | US | 2.2.0 | 2026-04-10 |
| OKC | Oklahoma City | US | 1.1.0 | 2026-04-10 |
| RTM | Rotterdam-The Hague | NL | 1.1.0 | 2026-04-10 |
| TPE | Taipei | TW | 1.2.0 | 2026-04-08 |
<!-- MAPS_TABLE:END -->

_The table above is regenerated automatically whenever a release manifest changes; don't edit it by hand._

## How to install

You'll need [Railyard](RAILYARD_LINK_TBD), the community map installer for Subway Builder. Once it's running:

1. Open Railyard and head to the **Browse** tab.
2. Add a new map source and paste the update URL for the map you want. The format is:
   ```
   https://raw.githubusercontent.com/ryandicicco/Subway-Builder-Maps/main/releases/{CODE}.json
   ```
   Swap `{CODE}` for any code from the table above; e.g. `CAI.json` for Cairo, `RTM.json` for Rotterdam-The Hague.
3. Railyard fetches the zip, installs it, and the map will show up in Subway Builder the next time you launch the game.

That's it. No manual file moving, no editing game files.

## Updates

Every map has a manifest at `releases/{CODE}.json` that Railyard checks for new versions. When I ship an update, Railyard notices, flags the new version in the app, and one click pulls it down. Full version history for each map lives in its JSON file if you want to see what changed and when.
