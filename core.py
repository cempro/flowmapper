# -*- coding: utf-8 -*-
"""Input parsing, flow calculations and shapefile writing for FlowMapper.

This module intentionally uses syntax supported by both Python 2.7 and
Python 3. QGIS/Qt imports live elsewhere so the calculation code can be
tested independently.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import io
import math
import os
import sys


try:
    text_type = unicode
except NameError:
    text_type = str


PY2 = sys.version_info[0] == 2
FLOW_TYPES = ("two_way", "gross", "net")
CURVE_BULGE_RATIO = 0.20
CURVE_SEGMENTS = 24


class FlowMapperError(Exception):
    """Raised for input or output problems that can be shown to the user."""


def _data_lines(path):
    """Yield non-empty, non-comment UTF-8 lines with their line numbers."""
    try:
        handle = io.open(path, "r", encoding="utf-8-sig")
    except (IOError, OSError) as exc:
        raise FlowMapperError("Could not open '{0}': {1}".format(path, exc))

    with handle:
        for line_number, raw_line in enumerate(handle, 1):
            line = raw_line.strip()
            if line and not line.startswith("#"):
                yield line_number, line


def _number(token, path, line_number, column_number):
    try:
        value = float(token)
    except (TypeError, ValueError):
        raise FlowMapperError(
            "Invalid number in '{0}' at row {1}, column {2}: {3}".format(
                path, line_number, column_number, token
            )
        )
    if math.isnan(value) or math.isinf(value):
        raise FlowMapperError(
            "Non-finite number in '{0}' at row {1}, column {2}.".format(
                path, line_number, column_number
            )
        )
    return value


def read_coordinates(path):
    """Read whitespace-delimited X Y coordinates."""
    coordinates = []
    for line_number, line in _data_lines(path):
        tokens = line.split()
        if len(tokens) != 2:
            raise FlowMapperError(
                "Coordinate row {0} in '{1}' must contain exactly X and Y.".format(
                    line_number, path
                )
            )
        x_value = _number(tokens[0], path, line_number, 1)
        y_value = _number(tokens[1], path, line_number, 2)
        coordinates.append((x_value, y_value))

    if not coordinates:
        raise FlowMapperError("The coordinate file contains no nodes: {0}".format(path))
    return coordinates


def read_names(path):
    """Read one UTF-8 node name per non-empty line, preserving spaces."""
    names = []
    try:
        handle = io.open(path, "r", encoding="utf-8-sig")
    except (IOError, OSError) as exc:
        raise FlowMapperError("Could not open '{0}': {1}".format(path, exc))

    with handle:
        for raw_line in handle:
            name = raw_line.strip()
            if name:
                names.append(name)

    if not names:
        raise FlowMapperError("The node-name file contains no names: {0}".format(path))
    return names


def read_matrix(path, node_count=None):
    """Read and validate a square whitespace-delimited flow matrix.

    The matrix row/column count is the authoritative node count.  The
    optional ``node_count`` argument is retained for callers that also want
    to assert an expected dimension.
    """
    source_rows = []
    for line_number, line in _data_lines(path):
        tokens = line.split()
        row = []
        for column_number, token in enumerate(tokens, 1):
            value = _number(token, path, line_number, column_number)
            if value < 0:
                raise FlowMapperError(
                    "Negative flow in '{0}' at row {1}, column {2}.".format(
                        path, line_number, column_number
                    )
                )
            row.append(value)
        source_rows.append((line_number, row))

    if not source_rows:
        raise FlowMapperError("The flow-matrix file contains no rows: {0}".format(path))

    matrix_size = len(source_rows)
    for line_number, row in source_rows:
        if len(row) != matrix_size:
            raise FlowMapperError(
                "Matrix row {0} in '{1}' has {2} values; a square {3} x {3} matrix requires {3}.".format(
                    line_number, path, len(row), matrix_size
                )
            )

    if node_count is not None and matrix_size != node_count:
        raise FlowMapperError(
            "The matrix in '{0}' has {1} rows; expected {2}.".format(
                path, matrix_size, node_count
            )
        )
    return [row for line_number, row in source_rows]


def load_inputs(coordinate_path, name_path, matrix_path):
    """Load FlowMapper text inputs and validate matching dimensions.

    Node names are optional.  When no name file is supplied, names are
    generated as node1, node2, ..., nodeN using the square matrix dimension.
    """
    matrix = read_matrix(matrix_path)
    node_count = len(matrix)
    coordinates = read_coordinates(coordinate_path)
    if len(coordinates) != node_count:
        raise FlowMapperError(
            "The flow matrix defines {0} nodes, but the coordinate file contains {1}.".format(
                node_count, len(coordinates)
            )
        )

    if name_path:
        names = read_names(name_path)
        if len(names) != node_count:
            raise FlowMapperError(
                "The flow matrix defines {0} nodes, but the name file contains {1} names.".format(
                    node_count, len(names)
                )
            )
    else:
        names = ["node{0}".format(index) for index in range(1, node_count + 1)]
    return coordinates, names, matrix


def format_magnitude(value):
    """Return a compact label matching the shapefile's six-decimal value."""
    rounded = float("{0:.6f}".format(float(value)))
    if abs(rounded - round(rounded)) < 1e-9:
        return text_type(int(round(rounded)))
    return ("{0:.6f}".format(rounded)).rstrip("0").rstrip(".")


def _normalize_flow_type(flow_type):
    normalized = text_type(flow_type).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized == "twoway":
        normalized = "two_way"
    if normalized not in FLOW_TYPES:
        raise FlowMapperError("Unknown flow type: {0}".format(flow_type))
    return normalized


def _haversine_km(point_a, point_b):
    """Great-circle distance for longitude/latitude pairs."""
    lon1, lat1 = point_a
    lon2, lat2 = point_b
    radians = math.pi / 180.0
    phi1 = lat1 * radians
    phi2 = lat2 * radians
    delta_phi = (lat2 - lat1) * radians
    delta_lambda = (lon2 - lon1) * radians
    hav = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    hav = min(1.0, max(0.0, hav))
    return 6371.0088 * 2.0 * math.atan2(math.sqrt(hav), math.sqrt(1.0 - hav))


def _planar_km(point_a, point_b, linear_units_to_meters):
    delta_x = point_b[0] - point_a[0]
    delta_y = point_b[1] - point_a[1]
    return math.sqrt(delta_x * delta_x + delta_y * delta_y) * linear_units_to_meters / 1000.0


def _flow_record(
    coordinates,
    names,
    from_index,
    to_index,
    magnitude,
    forward,
    reverse,
    flow_type,
    geographic,
    linear_units_to_meters,
):
    start = coordinates[from_index]
    end = coordinates[to_index]
    if geographic:
        length_km = _haversine_km(start, end)
    else:
        length_km = _planar_km(start, end, linear_units_to_meters)

    return {
        "from_id": from_index + 1,
        "to_id": to_index + 1,
        "from_name": names[from_index],
        "to_name": names[to_index],
        "from_x": start[0],
        "from_y": start[1],
        "to_x": end[0],
        "to_y": end[1],
        "magnitude": float(magnitude),
        "forward": float(forward),
        "reverse": float(reverse),
        "length_km": float(length_km),
        "flow_type": flow_type,
    }


def build_flow_records(
    coordinates,
    names,
    matrix,
    flow_type,
    include_self=False,
    include_zero=False,
    geographic=True,
    linear_units_to_meters=1.0,
):
    """Calculate directed line records for Two-way, Gross or Net flows.

    ``matrix[i][j]`` is interpreted as a flow from node i to node j.
    Net geometry follows the dominant direction. Gross geometry uses the
    lower-index node as its stable, non-semantic start point.
    """
    flow_type = _normalize_flow_type(flow_type)
    node_count = len(coordinates)
    if node_count != len(names) or node_count != len(matrix):
        raise FlowMapperError("Coordinates, names and matrix dimensions do not match.")
    for row in matrix:
        if len(row) != node_count:
            raise FlowMapperError("The flow matrix must be square.")

    records = []
    if flow_type == "two_way":
        for from_index in range(node_count):
            for to_index in range(node_count):
                if from_index == to_index and not include_self:
                    continue
                magnitude = matrix[from_index][to_index]
                if magnitude == 0 and not include_zero:
                    continue
                records.append(
                    _flow_record(
                        coordinates,
                        names,
                        from_index,
                        to_index,
                        magnitude,
                        matrix[from_index][to_index],
                        matrix[to_index][from_index],
                        flow_type,
                        geographic,
                        linear_units_to_meters,
                    )
                )
        return records

    for first_index in range(node_count):
        pair_start = first_index if include_self else first_index + 1
        for second_index in range(pair_start, node_count):
            first_to_second = matrix[first_index][second_index]
            second_to_first = matrix[second_index][first_index]

            if flow_type == "gross":
                if first_index == second_index:
                    magnitude = first_to_second
                else:
                    magnitude = first_to_second + second_to_first
                from_index = first_index
                to_index = second_index
            else:
                if first_index == second_index:
                    magnitude = first_to_second
                    from_index = first_index
                    to_index = second_index
                elif first_to_second >= second_to_first:
                    magnitude = first_to_second - second_to_first
                    from_index = first_index
                    to_index = second_index
                else:
                    magnitude = second_to_first - first_to_second
                    from_index = second_index
                    to_index = first_index

            if magnitude == 0 and not include_zero:
                continue
            records.append(
                _flow_record(
                    coordinates,
                    names,
                    from_index,
                    to_index,
                    magnitude,
                    matrix[from_index][to_index],
                    matrix[to_index][from_index],
                    flow_type,
                    geographic,
                    linear_units_to_meters,
                )
            )
    return records


def build_node_records(coordinates, names, matrix):
    """Calculate outgoing, incoming and signed net totals for every node.

    ``forward`` is the row total (outgoing), ``reverse`` is the column
    total (incoming), and ``net`` is ``forward - reverse``.  Diagonal values
    therefore contribute equally to outgoing and incoming totals and cancel
    in the signed net value.
    """
    node_count = len(coordinates)
    if node_count != len(names) or node_count != len(matrix):
        raise FlowMapperError("Coordinates, names and matrix dimensions do not match.")
    for row in matrix:
        if len(row) != node_count:
            raise FlowMapperError("The flow matrix must be square.")

    records = []
    for node_index in range(node_count):
        forward = float(sum(matrix[node_index]))
        reverse = float(
            sum(matrix[row_index][node_index] for row_index in range(node_count))
        )
        net = forward - reverse
        tolerance = 1e-9 * max(1.0, abs(forward), abs(reverse))
        if abs(net) <= tolerance:
            net = 0.0
            gain_loss = "balanced"
        elif net < 0:
            gain_loss = "gain"
        else:
            gain_loss = "loss"
        coordinate = coordinates[node_index]
        records.append(
            {
                "node_id": node_index + 1,
                "node_name": names[node_index],
                "forward": forward,
                "reverse": reverse,
                "net": net,
                "gain_loss": gain_loss,
                "coord_x": coordinate[0],
                "coord_y": coordinate[1],
            }
        )
    return records


def _load_ogr():
    try:
        from osgeo import gdal, ogr, osr
        return gdal, ogr, osr
    except ImportError:
        try:
            import gdal
            import ogr
            import osr
            return gdal, ogr, osr
        except ImportError:
            raise FlowMapperError(
                "GDAL/OGR Python bindings are unavailable. Use the Python environment bundled with QGIS."
            )


def _ogr_path(path):
    if PY2 and isinstance(path, text_type):
        return path.encode("utf-8")
    return path


def _ogr_ascii(value):
    """Use native ASCII byte strings for older Python 2 GDAL/SWIG builds."""
    if PY2 and isinstance(value, text_type):
        return value.encode("ascii")
    return value


def _ogr_text(value):
    value = text_type(value)
    if len(value) > 254:
        value = value[:254]
    if PY2:
        return value.encode("utf-8")
    return value


def _create_spatial_reference(osr, epsg):
    spatial_reference = osr.SpatialReference()
    result = spatial_reference.ImportFromEPSG(int(epsg))
    if result != 0:
        raise FlowMapperError("EPSG:{0} could not be loaded.".format(epsg))
    if hasattr(spatial_reference, "SetAxisMappingStrategy") and hasattr(
        osr, "OAMS_TRADITIONAL_GIS_ORDER"
    ):
        spatial_reference.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return spatial_reference


def _validate_geographic_coordinates(coordinates):
    for index, coordinate in enumerate(coordinates, 1):
        longitude, latitude = coordinate
        if longitude < -180 or longitude > 180 or latitude < -90 or latitude > 90:
            raise FlowMapperError(
                "Node {0} is outside longitude/latitude limits for a geographic CRS.".format(index)
            )


def _add_field(layer, ogr, name, field_type, width=None, precision=None):
    field = ogr.FieldDefn(_ogr_ascii(name), field_type)
    if width is not None:
        field.SetWidth(width)
    if precision is not None:
        field.SetPrecision(precision)
    if layer.CreateField(field) != 0:
        raise FlowMapperError("Could not create output field: {0}".format(name))


def curved_line_points(point_a, point_b):
    """Approximate a smooth quadratic Bezier curve with line vertices.

    The visible midpoint bulge is ``CURVE_BULGE_RATIO`` of the node-to-node
    distance.  Reversing the flow direction automatically bends the curve to
    the opposite side, keeping Two-way flows visually separate.
    """
    start_x, start_y = point_a
    end_x, end_y = point_b
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    if distance == 0:
        return [point_a, point_b]

    normal_x = -delta_y / distance
    normal_y = delta_x / distance
    control_offset = 2.0 * CURVE_BULGE_RATIO * distance
    control_x = (start_x + end_x) / 2.0 + normal_x * control_offset
    control_y = (start_y + end_y) / 2.0 + normal_y * control_offset

    points = []
    for segment in range(CURVE_SEGMENTS + 1):
        t_value = segment / float(CURVE_SEGMENTS)
        inverse = 1.0 - t_value
        x_value = (
            inverse * inverse * start_x
            + 2.0 * inverse * t_value * control_x
            + t_value * t_value * end_x
        )
        y_value = (
            inverse * inverse * start_y
            + 2.0 * inverse * t_value * control_y
            + t_value * t_value * end_y
        )
        points.append((x_value, y_value))
    return points


def write_flow_shapefile(output_path, records, epsg, curved=False):
    """Write calculated records to an ESRI Shapefile using QGIS's GDAL."""
    gdal, ogr, osr = _load_ogr()
    ogr.UseExceptions()
    gdal.SetConfigOption(_ogr_ascii("GDAL_FILENAME_IS_UTF8"), _ogr_ascii("YES"))
    gdal.SetConfigOption(_ogr_ascii("SHAPE_ENCODING"), _ogr_ascii("UTF-8"))

    output_path = os.path.abspath(output_path)
    if not output_path.lower().endswith(".shp"):
        output_path += ".shp"
    output_directory = os.path.dirname(output_path)
    if not os.path.isdir(output_directory):
        raise FlowMapperError("Output folder does not exist: {0}".format(output_directory))

    driver = ogr.GetDriverByName(_ogr_ascii("ESRI Shapefile"))
    if driver is None:
        raise FlowMapperError("The ESRI Shapefile GDAL driver is unavailable.")

    ogr_output_path = _ogr_path(output_path)
    if os.path.exists(output_path):
        if driver.DeleteDataSource(ogr_output_path) != 0:
            raise FlowMapperError(
                "The existing shapefile could not be replaced. Remove it from QGIS and try again."
            )

    spatial_reference = _create_spatial_reference(osr, epsg)
    data_source = driver.CreateDataSource(ogr_output_path)
    if data_source is None:
        raise FlowMapperError("Could not create output shapefile: {0}".format(output_path))

    try:
        layer = data_source.CreateLayer(
            _ogr_ascii("flow_lines"),
            spatial_reference,
            ogr.wkbLineString,
            [_ogr_ascii("ENCODING=UTF-8")],
        )
        if layer is None:
            raise FlowMapperError("Could not create the flow-lines layer.")

        _add_field(layer, ogr, "flow_id", ogr.OFTInteger)
        _add_field(layer, ogr, "from_id", ogr.OFTInteger)
        _add_field(layer, ogr, "to_id", ogr.OFTInteger)
        _add_field(layer, ogr, "from_name", ogr.OFTString, 254)
        _add_field(layer, ogr, "to_name", ogr.OFTString, 254)
        _add_field(layer, ogr, "name_x1y1", ogr.OFTString, 254)
        _add_field(layer, ogr, "name_x2y2", ogr.OFTString, 254)
        _add_field(layer, ogr, "magnitude", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "mag_label", ogr.OFTString, 32)
        _add_field(layer, ogr, "forward", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "reverse", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "length_km", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "coord_x1", ogr.OFTReal, 24, 10)
        _add_field(layer, ogr, "coord_y1", ogr.OFTReal, 24, 10)
        _add_field(layer, ogr, "coord_x2", ogr.OFTReal, 24, 10)
        _add_field(layer, ogr, "coord_y2", ogr.OFTReal, 24, 10)
        _add_field(layer, ogr, "flow_type", ogr.OFTString, 12)

        layer_definition = layer.GetLayerDefn()
        for flow_id, record in enumerate(records, 1):
            geometry = ogr.Geometry(ogr.wkbLineString)
            start_point = (record["from_x"], record["from_y"])
            end_point = (record["to_x"], record["to_y"])
            if curved:
                geometry_points = curved_line_points(start_point, end_point)
            else:
                geometry_points = [start_point, end_point]
            for x_value, y_value in geometry_points:
                geometry.AddPoint(x_value, y_value)

            feature = ogr.Feature(layer_definition)
            feature.SetGeometry(geometry)
            feature.SetField(_ogr_ascii("flow_id"), flow_id)
            feature.SetField(_ogr_ascii("from_id"), record["from_id"])
            feature.SetField(_ogr_ascii("to_id"), record["to_id"])
            feature.SetField(_ogr_ascii("from_name"), _ogr_text(record["from_name"]))
            feature.SetField(_ogr_ascii("to_name"), _ogr_text(record["to_name"]))
            feature.SetField(_ogr_ascii("name_x1y1"), _ogr_text(record["from_name"]))
            feature.SetField(_ogr_ascii("name_x2y2"), _ogr_text(record["to_name"]))
            feature.SetField(_ogr_ascii("magnitude"), record["magnitude"])
            feature.SetField(
                _ogr_ascii("mag_label"), _ogr_text(format_magnitude(record["magnitude"]))
            )
            feature.SetField(_ogr_ascii("forward"), record["forward"])
            feature.SetField(_ogr_ascii("reverse"), record["reverse"])
            feature.SetField(_ogr_ascii("length_km"), record["length_km"])
            feature.SetField(_ogr_ascii("coord_x1"), record["from_x"])
            feature.SetField(_ogr_ascii("coord_y1"), record["from_y"])
            feature.SetField(_ogr_ascii("coord_x2"), record["to_x"])
            feature.SetField(_ogr_ascii("coord_y2"), record["to_y"])
            feature.SetField(_ogr_ascii("flow_type"), _ogr_text(record["flow_type"]))
            if layer.CreateFeature(feature) != 0:
                raise FlowMapperError("Could not write flow feature {0}.".format(flow_id))
            feature = None
            geometry = None

        layer.SyncToDisk()
    except Exception:
        data_source = None
        if os.path.exists(output_path):
            try:
                driver.DeleteDataSource(ogr_output_path)
            except Exception:
                pass
        raise
    finally:
        data_source = None

    _write_utf8_cpg(output_path)
    return output_path


def _write_utf8_cpg(output_path):
    """Write the Shapefile encoding sidecar when GDAL did not create one."""
    cpg_path = os.path.splitext(output_path)[0] + ".cpg"
    if not os.path.exists(cpg_path):
        try:
            with io.open(cpg_path, "w", encoding="ascii") as cpg_file:
                cpg_file.write("UTF-8\n")
        except (IOError, OSError):
            pass


def write_node_shapefile(output_path, records, epsg):
    """Write node totals as an ESRI point Shapefile using QGIS's GDAL."""
    gdal, ogr, osr = _load_ogr()
    ogr.UseExceptions()
    gdal.SetConfigOption(_ogr_ascii("GDAL_FILENAME_IS_UTF8"), _ogr_ascii("YES"))
    gdal.SetConfigOption(_ogr_ascii("SHAPE_ENCODING"), _ogr_ascii("UTF-8"))

    output_path = os.path.abspath(output_path)
    if not output_path.lower().endswith(".shp"):
        output_path += ".shp"
    output_directory = os.path.dirname(output_path)
    if not os.path.isdir(output_directory):
        raise FlowMapperError("Output folder does not exist: {0}".format(output_directory))

    driver = ogr.GetDriverByName(_ogr_ascii("ESRI Shapefile"))
    if driver is None:
        raise FlowMapperError("The ESRI Shapefile GDAL driver is unavailable.")

    ogr_output_path = _ogr_path(output_path)
    if os.path.exists(output_path):
        if driver.DeleteDataSource(ogr_output_path) != 0:
            raise FlowMapperError(
                "The existing node shapefile could not be replaced. Remove it from QGIS and try again."
            )

    spatial_reference = _create_spatial_reference(osr, epsg)
    data_source = driver.CreateDataSource(ogr_output_path)
    if data_source is None:
        raise FlowMapperError("Could not create output shapefile: {0}".format(output_path))

    try:
        layer = data_source.CreateLayer(
            _ogr_ascii("flow_nodes"),
            spatial_reference,
            ogr.wkbPoint,
            [_ogr_ascii("ENCODING=UTF-8")],
        )
        if layer is None:
            raise FlowMapperError("Could not create the flow-nodes layer.")

        _add_field(layer, ogr, "node_id", ogr.OFTInteger)
        _add_field(layer, ogr, "node_name", ogr.OFTString, 254)
        _add_field(layer, ogr, "forward", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "reverse", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "net", ogr.OFTReal, 24, 6)
        _add_field(layer, ogr, "gain_loss", ogr.OFTString, 8)
        _add_field(layer, ogr, "coord_x", ogr.OFTReal, 24, 10)
        _add_field(layer, ogr, "coord_y", ogr.OFTReal, 24, 10)

        layer_definition = layer.GetLayerDefn()
        for record in records:
            geometry = ogr.Geometry(ogr.wkbPoint)
            geometry.AddPoint(record["coord_x"], record["coord_y"])

            feature = ogr.Feature(layer_definition)
            feature.SetGeometry(geometry)
            feature.SetField(_ogr_ascii("node_id"), record["node_id"])
            feature.SetField(_ogr_ascii("node_name"), _ogr_text(record["node_name"]))
            feature.SetField(_ogr_ascii("forward"), record["forward"])
            feature.SetField(_ogr_ascii("reverse"), record["reverse"])
            feature.SetField(_ogr_ascii("net"), record["net"])
            feature.SetField(_ogr_ascii("gain_loss"), _ogr_text(record["gain_loss"]))
            feature.SetField(_ogr_ascii("coord_x"), record["coord_x"])
            feature.SetField(_ogr_ascii("coord_y"), record["coord_y"])
            if layer.CreateFeature(feature) != 0:
                raise FlowMapperError(
                    "Could not write node feature {0}.".format(record["node_id"])
                )
            feature = None
            geometry = None

        layer.SyncToDisk()
    except Exception:
        data_source = None
        if os.path.exists(output_path):
            try:
                driver.DeleteDataSource(ogr_output_path)
            except Exception:
                pass
        raise
    finally:
        data_source = None

    _write_utf8_cpg(output_path)
    return output_path


def create_flow_shapefile(
    coordinate_path,
    name_path,
    matrix_path,
    output_path,
    flow_type,
    epsg=4326,
    include_self=False,
    include_zero=False,
    curved=False,
):
    """Run the complete input-to-shapefile workflow."""
    coordinates, names, matrix = load_inputs(coordinate_path, name_path, matrix_path)
    gdal, ogr, osr = _load_ogr()
    spatial_reference = _create_spatial_reference(osr, epsg)
    geographic = bool(spatial_reference.IsGeographic())
    if geographic:
        _validate_geographic_coordinates(coordinates)
        linear_units_to_meters = 1.0
    else:
        try:
            linear_units_to_meters = float(spatial_reference.GetLinearUnits())
        except (TypeError, ValueError):
            linear_units_to_meters = 1.0

    records = build_flow_records(
        coordinates,
        names,
        matrix,
        flow_type,
        include_self=include_self,
        include_zero=include_zero,
        geographic=geographic,
        linear_units_to_meters=linear_units_to_meters,
    )
    try:
        output_path = write_flow_shapefile(
            output_path, records, epsg, curved=curved
        )
    except FlowMapperError:
        raise
    except Exception as exc:
        raise FlowMapperError("GDAL/OGR could not create the shapefile: {0}".format(exc))
    return {
        "path": output_path,
        "feature_count": len(records),
        "node_count": len(coordinates),
        "flow_type": _normalize_flow_type(flow_type),
        "line_shape": "curved" if curved else "straight",
    }


def create_node_shapefile(
    coordinate_path,
    name_path,
    matrix_path,
    output_path,
    epsg=4326,
):
    """Create the optional point layer containing per-node flow totals."""
    coordinates, names, matrix = load_inputs(coordinate_path, name_path, matrix_path)
    gdal, ogr, osr = _load_ogr()
    spatial_reference = _create_spatial_reference(osr, epsg)
    if spatial_reference.IsGeographic():
        _validate_geographic_coordinates(coordinates)

    records = build_node_records(coordinates, names, matrix)
    try:
        output_path = write_node_shapefile(output_path, records, epsg)
    except FlowMapperError:
        raise
    except Exception as exc:
        raise FlowMapperError(
            "GDAL/OGR could not create the node shapefile: {0}".format(exc)
        )
    return {
        "path": output_path,
        "feature_count": len(records),
        "node_count": len(records),
    }
