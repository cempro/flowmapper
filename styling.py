# -*- coding: utf-8 -*-
"""Cross-version map presentation for FlowMapper output layers."""

from __future__ import absolute_import, unicode_literals

from .qt_compat import QGIS3, QtGui, text_type


LINE_COLOR = "44,104,180"
LINE_WIDTH_MM = 0.6
ARROW_SIZE_MM = 2.0
TWO_WAY_OFFSET_MM = 0.8
NODE_SIZE_MM = 3.6
GAIN_COLOR = "46,160,67"
LOSS_COLOR = "215,48,39"
BALANCED_COLOR = "128,128,128"


def apply_layer_presentation(layer, flow_type):
    """Apply basic line styling, arrows and magnitude labels.

    Presentation errors are returned instead of aborting creation of a valid
    shapefile.  This keeps the core result usable across the wide range of
    QGIS 2.x and QGIS 3.x point releases.
    """
    warnings = []
    try:
        if QGIS3:
            _style_qgis3(layer, flow_type)
        else:
            _style_qgis2(layer, flow_type)
    except Exception as exc:
        warnings.append("automatic line styling: {0}".format(text_type(exc)))

    try:
        if QGIS3:
            _label_qgis3(layer)
        else:
            _label_qgis2(layer)
    except Exception as exc:
        warnings.append("magnitude labels: {0}".format(text_type(exc)))

    try:
        layer.triggerRepaint()
    except Exception:
        pass
    return warnings


def apply_node_presentation(layer):
    """Color flow nodes as gain, loss or balanced in QGIS 2 and QGIS 3."""
    warnings = []
    try:
        if QGIS3:
            _style_nodes_qgis3(layer)
        else:
            _style_nodes_qgis2(layer)
    except Exception as exc:
        warnings.append("gain/loss node styling: {0}".format(text_type(exc)))

    try:
        layer.triggerRepaint()
    except Exception:
        pass
    return warnings


def _style_nodes_qgis3(layer):
    from qgis.core import (
        QgsCategorizedSymbolRenderer,
        QgsMarkerSymbol,
        QgsRendererCategory,
    )

    categories = []
    definitions = (
        ("gain", GAIN_COLOR, "Gain"),
        ("balanced", BALANCED_COLOR, "Balanced"),
        ("loss", LOSS_COLOR, "Loss"),
    )
    for value, color, label in definitions:
        symbol = QgsMarkerSymbol.createSimple(
            {
                "name": "circle",
                "color": color,
                "outline_color": "70,70,70",
                "outline_width": "0.25",
                "size": str(NODE_SIZE_MM),
            }
        )
        categories.append(QgsRendererCategory(value, symbol, label))
    layer.setRenderer(QgsCategorizedSymbolRenderer("gain_loss", categories))


def _style_nodes_qgis2(layer):
    from qgis.core import (
        QgsCategorizedSymbolRendererV2,
        QgsMarkerSymbolV2,
        QgsRendererCategoryV2,
    )

    categories = []
    definitions = (
        ("gain", GAIN_COLOR, "Gain"),
        ("balanced", BALANCED_COLOR, "Balanced"),
        ("loss", LOSS_COLOR, "Loss"),
    )
    for value, color, label in definitions:
        symbol = QgsMarkerSymbolV2.createSimple(
            {
                "name": "circle",
                "color": color,
                "color_border": "70,70,70",
                "outline_width": "0.25",
                "size": str(NODE_SIZE_MM),
            }
        )
        categories.append(QgsRendererCategoryV2(value, symbol, label))
    layer.setRendererV2(QgsCategorizedSymbolRendererV2("gain_loss", categories))


def _qgis3_marker_placement(marker_layer_class, placement_name):
    if hasattr(marker_layer_class, placement_name):
        return getattr(marker_layer_class, placement_name)
    try:
        from qgis.core import Qgis

        placement_enum = getattr(Qgis, "MarkerLinePlacement", None)
        if placement_enum is not None:
            return getattr(placement_enum, placement_name, None)
    except (ImportError, AttributeError):
        pass
    return None


def _style_qgis3(layer, flow_type):
    from qgis.core import (
        QgsLineSymbol,
        QgsMarkerLineSymbolLayer,
        QgsMarkerSymbol,
        QgsSingleSymbolRenderer,
    )

    offset = TWO_WAY_OFFSET_MM if flow_type == "two_way" else 0.0
    symbol = QgsLineSymbol.createSimple(
        {
            "color": LINE_COLOR,
            "width": str(LINE_WIDTH_MM),
            "offset": str(offset),
        }
    )

    if flow_type in ("two_way", "net"):
        if flow_type == "net":
            placement_property = "centralpoint"
            placement_name = "CentralPoint"
        else:
            placement_property = "lastvertex"
            placement_name = "LastVertex"
        marker_line = QgsMarkerLineSymbolLayer.create(
            {"placement": placement_property, "rotate": "1"}
        )
        if marker_line is None:
            marker_line = QgsMarkerLineSymbolLayer()
        marker_symbol = QgsMarkerSymbol.createSimple(
            {
                "name": "filled_arrowhead",
                "color": LINE_COLOR,
                "outline_color": LINE_COLOR,
                "size": str(ARROW_SIZE_MM),
            }
        )
        marker_line.setSubSymbol(marker_symbol)
        placement = _qgis3_marker_placement(
            QgsMarkerLineSymbolLayer, placement_name
        )
        if placement is not None:
            marker_line.setPlacement(placement)
        if hasattr(marker_line, "setRotateSymbols"):
            marker_line.setRotateSymbols(True)
        elif hasattr(marker_line, "setRotateMarker"):
            marker_line.setRotateMarker(True)
        marker_line.setOffset(offset)
        symbol.appendSymbolLayer(marker_line)

    layer.setRenderer(QgsSingleSymbolRenderer(symbol))


def _style_qgis2(layer, flow_type):
    from qgis.core import (
        QgsLineSymbolV2,
        QgsMarkerLineSymbolLayerV2,
        QgsMarkerSymbolV2,
        QgsSingleSymbolRendererV2,
    )

    offset = TWO_WAY_OFFSET_MM if flow_type == "two_way" else 0.0
    symbol = QgsLineSymbolV2.createSimple(
        {
            "color": LINE_COLOR,
            "width": str(LINE_WIDTH_MM),
            "offset": str(offset),
        }
    )

    if flow_type in ("two_way", "net"):
        if flow_type == "net":
            placement_property = "centralpoint"
            placement = QgsMarkerLineSymbolLayerV2.CentralPoint
        else:
            placement_property = "lastvertex"
            placement = QgsMarkerLineSymbolLayerV2.LastVertex
        marker_line = QgsMarkerLineSymbolLayerV2.create(
            {"placement": placement_property, "rotate": "1"}
        )
        if marker_line is None:
            marker_line = QgsMarkerLineSymbolLayerV2()
        marker_symbol = QgsMarkerSymbolV2.createSimple(
            {
                "name": "filled_arrowhead",
                "color": LINE_COLOR,
                "color_border": LINE_COLOR,
                "size": str(ARROW_SIZE_MM),
            }
        )
        marker_line.setSubSymbol(marker_symbol)
        marker_line.setPlacement(placement)
        marker_line.setRotateMarker(True)
        marker_line.setOffset(offset)
        symbol.appendSymbolLayer(marker_line)

    layer.setRendererV2(QgsSingleSymbolRendererV2(symbol))


def _qgis3_line_placement(settings_class):
    if hasattr(settings_class, "Line"):
        return settings_class.Line
    from qgis.core import Qgis

    return Qgis.LabelPlacement.Line


def _set_qgis3_above_line(settings, settings_class):
    """Place labels relative to direction so reverse lines use opposite sides."""
    if hasattr(settings, "placementFlags") and hasattr(settings_class, "AboveLine"):
        settings.placementFlags = settings_class.AboveLine
        return

    if not hasattr(settings, "lineSettings"):
        return
    try:
        from qgis.core import Qgis

        flag_enum = getattr(Qgis, "LabelLinePlacementFlag", None)
        if flag_enum is None:
            return
        line_settings = settings.lineSettings()
        line_settings.setPlacementFlags(flag_enum.AboveLine)
        settings.setLineSettings(line_settings)
    except (AttributeError, TypeError):
        pass


def _label_qgis3(layer):
    from qgis.core import (
        QgsPalLayerSettings,
        QgsTextBufferSettings,
        QgsTextFormat,
        QgsVectorLayerSimpleLabeling,
    )

    settings = QgsPalLayerSettings()
    settings.enabled = True
    settings.fieldName = "mag_label"
    settings.isExpression = False
    settings.placement = _qgis3_line_placement(QgsPalLayerSettings)
    _set_qgis3_above_line(settings, QgsPalLayerSettings)
    if hasattr(settings, "dist"):
        settings.dist = 1.5
    if hasattr(settings, "distInMapUnits"):
        settings.distInMapUnits = False
    if hasattr(settings, "displayAll"):
        settings.displayAll = True

    text_format = QgsTextFormat()
    text_format.setSize(9.0)
    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(0.8)
    buffer_settings.setColor(QtGui.QColor("white"))
    text_format.setBuffer(buffer_settings)
    settings.setFormat(text_format)

    layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
    layer.setLabelsEnabled(True)


def _label_qgis2(layer):
    from qgis.core import QgsPalLayerSettings

    settings = QgsPalLayerSettings()
    settings.readFromLayer(layer)
    settings.enabled = True
    settings.fieldName = "mag_label"
    settings.isExpression = False
    settings.placement = QgsPalLayerSettings.Line
    settings.placementFlags = QgsPalLayerSettings.AboveLine
    settings.dist = 1.5
    if hasattr(settings, "distInMapUnits"):
        settings.distInMapUnits = False
    if hasattr(settings, "displayAll"):
        settings.displayAll = True

    font = QtGui.QFont(settings.textFont)
    font.setPointSizeF(9.0)
    settings.textFont = font
    settings.bufferDraw = True
    settings.bufferSize = 0.8
    settings.bufferColor = QtGui.QColor("white")
    if hasattr(settings, "bufferSizeInMapUnits"):
        settings.bufferSizeInMapUnits = False
    settings.writeToLayer(layer)
