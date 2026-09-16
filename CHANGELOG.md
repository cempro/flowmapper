# Changelog

## 1.0.0 — 2026-09-16

- Rewrote the core plugin with one Python 2.7/Python 3 codebase.
- Added a PyQt4/PyQt5 compatibility layer for QGIS 2.x and QGIS 3.x.
- Reimplemented Two-way, Gross and Net flow calculations.
- Added strict validation for coordinate, optional name and square matrix inputs.
- Generate `node1` through `nodeN` when the node-name file is omitted.
- Preserved UTF-8 node names and added explicit source/target attributes.
- Retained `name_x1y1` and `name_x2y2` aliases for field compatibility.
- Added EPSG selection and kilometre length calculation.
- Added optional zero-flow and diagonal/self-flow handling.
- Added compact magnitude labels, directional arrows and Two-way line offsets.
- Added mutually exclusive straight/curved flow-line options, with straight lines as the default.
- Place Net arrows at the line center and Two-way arrows at the last vertex.
- Added an optional point Shapefile with per-node outgoing (`forward`), incoming (`reverse`) and signed `net` totals.
- Added optional gain/loss node coloring: gain is green, loss is red and balanced is gray.
- Added output-to-map options and an About dialog with a dedicated icon.
- Marked the plugin as non-experimental in metadata.
- Deferred advanced classified symbology and filters to a later release.
