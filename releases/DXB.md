# Dubai

### DXB · 1.2.0

Highly-detailed map of the Greater Dubai area using 2024 Dubai Statistics Center community population data, WorldPop 100m density rasters, and a curated 43-zone employment dataset. Commute matrix built with a v5 doubly-constrained gravity model tuned for a Dubai-realistic distance profile.

![Map Preview](screenshot1.png)

## Coverage

<table style="width: auto">
<tr><td><strong>Region</strong></td><td>Greater Dubai (Emirate of Dubai, coastal strip + inland communities)</td></tr>
<tr><td><strong>Communities Modeled</strong></td><td>224 (DSC 2024)</td></tr>
<tr><td><strong>OSM-Matched Boundaries</strong></td><td>120</td></tr>
<tr><td><strong>Playable Bbox</strong></td><td>~73.6 km × 70.2 km (≈5,167 km² bounding box; ocean and desert excluded at runtime)</td></tr>
</table>

<details>
<summary>Top communities by population</summary>

<table style="width: auto">
<tr><th align="left">Code</th><th align="left">Community</th><th align="right">Population (2024)</th></tr>
<tr><td>599</td><td>Jabal Ali Industrial First</td><td align="right">205,079</td></tr>
<tr><td>264</td><td>Muhaisanah Second</td><td align="right">160,831</td></tr>
<tr><td>365</td><td>Al Qouz Industrial Second</td><td align="right">144,327</td></tr>
<tr><td>621</td><td>Warsan First</td><td align="right">120,353</td></tr>
<tr><td>591</td><td>Jabal Ali First</td><td align="right">96,005</td></tr>
<tr><td>127</td><td>Hor Al Anz</td><td align="right">92,239</td></tr>
<tr><td>597</td><td>Dubai Investment Park Second</td><td align="right">88,789</td></tr>
<tr><td>318</td><td>Al Karama</td><td align="right">82,625</td></tr>
<tr><td>392</td><td>Marsa Dubai (Dubai Marina)</td><td align="right">78,843</td></tr>
<tr><td>124</td><td>Al Murqabat</td><td align="right">78,016</td></tr>
<tr><td>598</td><td>Dubai Investment Park First</td><td align="right">75,316</td></tr>
<tr><td>251</td><td>Mirdif</td><td align="right">74,135</td></tr>
<tr><td>241</td><td>Al Nahda Second</td><td align="right">71,100</td></tr>
<tr><td>333</td><td>Al Bada'</td><td align="right">63,592</td></tr>
<tr><td>358</td><td>Al Qouz Third</td><td align="right">61,353</td></tr>
</table>

_Full list: 224 communities totalling 4,248,200 residents (DSC Population Bulletin 2024)._

</details>

## Population Summary

<table style="width: auto">
<tr><td><strong>DSC 2024 Total Population</strong></td><td align="right">4,248,200</td></tr>
<tr><td><strong>Modeled Residents (working-age subset)</strong></td><td align="right">3,105,983</td></tr>
<tr><td><strong>Modeled Jobs</strong></td><td align="right">3,105,983</td></tr>
<tr><td><strong>Total Modeled Demand (commute pops)</strong></td><td align="right">3,105,983</td></tr>
<tr><td><strong>Commute OD Pairs</strong></td><td align="right">195,806</td></tr>
</table>

_Residents in the in-game `points[].residents` field reflect the **working-age population** (≈73.1% of DSC's 4.25M total), so the resident total matches the job/commute total 1:1 as the demand schema expects. Children, retirees, and non-working residents are counted toward the city's overall DSC total but not toward modeled commute demand._

## Map Statistics

<table style="width: auto">
<tr><td><strong>Buildings Indexed</strong></td><td align="right">361,640</td></tr>
<tr><td><strong>Resident Points</strong></td><td align="right">10,323</td></tr>
<tr><td><strong>Job Points</strong></td><td align="right">1,392</td></tr>
<tr><td><strong>Named Employment Zones</strong></td><td align="right">43</td></tr>
<tr><td><strong>Size-Weighted Median Commute</strong></td><td align="right">7.1 km · 12.2 min</td></tr>
<tr><td><strong>Mean Commute</strong></td><td align="right">9.7 km · 14.2 min</td></tr>
<tr><td><strong>Share &lt; 1.5 km</strong></td><td align="right">3.9%</td></tr>
<tr><td><strong>Share &gt; 5 km</strong></td><td align="right">58.3%</td></tr>
<tr><td><strong>Share &gt; 10 km</strong></td><td align="right">22.6%</td></tr>
</table>

## Additional Features

- **Building Collision** — A 361,640-entry buildings index provides in-game collision geometry for all non-filtered buildings in the Dubai bbox.
- **Ocean Foundations** — Ocean bathymetry layer included for the Persian Gulf coastline.
- **Labels** — 7 cities, 299 suburbs, and 63 neighborhood labels rendered via a `name:en`-first fallback chain across zoom levels 6–15. Pulled from OSM `admin_level=10` + `place=suburb|neighbourhood` relations.
- **Runways & Taxiways** — DXB (Dubai International) and DWC (Al Maktoum) airport layouts included as a dedicated GeoJSON layer.

## Methodology

Demand is built from the ground up rather than bulk-imported:

1. **Residents (3,105,983 modeled; 4,248,200 DSC total).** WorldPop UAE 100m raster aggregated to a ~250m grid. Cells that fall inside OSM `admin_level=10` polygons fuzzy-matched to DSC community names are rescaled to hit the exact DSC 2024 per-community total (4,248,200 total). After gravity matrix generation, the per-point resident counts are scaled to the working-age subset (≈73.1%) so `sum(points[].residents) == sum(pops[].size)` as Railyard's schema expects. 31 top unmatched communities use hand-curated bboxes; residual population is absorbed by WorldPop-weighted unassigned cells, so per-community totals remain proportional to DSC.
2. **Jobs (3,105,983).** 43 curated named employment zones (DIFC, Downtown, Business Bay, Media/Internet City, Marina/JLT, DAFZA, Dubai South, the free zones, etc.) cover the anchor employers. Four distributed categories (household services, construction labor, public services, distributed retail) are placed proportional to residential density.
3. **Commute Matrix (v5 gravity).** Doubly-constrained IPF gravity model with `alpha = 1.0`, `top_k = 25` destinations per origin, and a **5 km deterrence floor** — trips shorter than 5 km all share the same gravity weight so the model doesn't preferentially match residents to the nearest walkable job. Mass-preserving stochastic rounding keeps the integer total exact. Result: size-weighted median commute 12.2 min / 7.1 km, share < 1.5 km = 3.9% (was 39% with the old gravity), share > 5 km = 58.3%. In-game walking mode share lands near ~5%.

## Data Sources

- **Dubai Statistics Center (DSC) Population Bulletin 2024** — community-level resident totals (224 communities, 4,248,200 total).
- **WorldPop UAE 2020 100m constrained population grid** (https://www.worldpop.org) — residential density rasters, redistributed to DSC totals.
- **OpenStreetMap** — `admin_level=10` community polygons, `place=suburb`/`place=neighbourhood` labels, building footprints, road network, runway/taxiway geometry. © OpenStreetMap contributors, ODbL.
- **Kontur Population v3** / **Natural Earth** — coastline and bathymetry support layers.

## License

Map data derived from OpenStreetMap is licensed under [ODbL](https://opendatacommons.org/licenses/odbl/). DSC figures are cited from publicly-released government bulletins. The map pack itself (compiled PMTiles, demand_data.json, config, scripts) is released under CC BY 4.0 — please credit `Ryan DiCicco (rdicicco)` if you reuse the pipeline.

## Credits

Map authored by Ryan DiCicco (rdicicco) · Data pipeline in [Subway-Builder-Maps](https://github.com/ryandicicco/Subway-Builder-Maps) · Built for [Railyard](https://subwaybuildermodded.com/railyard/).
