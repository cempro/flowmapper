# -*- coding: utf-8 -*-
"""QGIS plugin integration for FlowMapper."""

from __future__ import absolute_import, unicode_literals

import os

from .core import FlowMapperError, create_flow_shapefile, create_node_shapefile
from .dialog import AboutDialog, FlowMapperDialog
from .qt_compat import QtCore, QtGui, QtWidgets, text_type
from .styling import apply_layer_presentation, apply_node_presentation


class FlowMapper(object):
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.menu_name = "&FlowMapper"
        self.main_action = None
        self.about_action = None
        self.dialog = None

    def initGui(self):
        icon = QtGui.QIcon(os.path.join(self.plugin_dir, "icon.png"))
        about_icon = QtGui.QIcon(os.path.join(self.plugin_dir, "about.png"))
        self.main_action = QtWidgets.QAction(
            icon, "Generate flow lines", self.iface.mainWindow()
        )
        self.main_action.setObjectName("FlowMapperGenerateAction")
        self.main_action.setStatusTip("Generate Two-way, Gross or Net flow lines")
        self.main_action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.menu_name, self.main_action)
        self.iface.addToolBarIcon(self.main_action)

        self.about_action = QtWidgets.QAction(
            about_icon, "About FlowMapper", self.iface.mainWindow()
        )
        self.about_action.setObjectName("FlowMapperAboutAction")
        self.about_action.triggered.connect(self.show_about)
        self.iface.addPluginToMenu(self.menu_name, self.about_action)

    def unload(self):
        if self.main_action is not None:
            self.iface.removePluginMenu(self.menu_name, self.main_action)
            self.iface.removeToolBarIcon(self.main_action)
        if self.about_action is not None:
            self.iface.removePluginMenu(self.menu_name, self.about_action)
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

    def run(self):
        if self.dialog is None:
            self.dialog = FlowMapperDialog(self.iface.mainWindow())
            self.dialog.about_button.setIcon(
                QtGui.QIcon(os.path.join(self.plugin_dir, "about.png"))
            )
            self.dialog.generate_button.clicked.connect(self.generate)
            self.dialog.about_button.clicked.connect(self.show_about)
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def show_about(self):
        dialog = AboutDialog(self.iface.mainWindow())
        dialog.exec_()

    def _validate_paths(self, values):
        labels = (
            ("coordinate_path", "node coordinate file"),
            ("matrix_path", "flow-matrix file"),
        )
        for key, label in labels:
            path = values[key]
            if not path:
                raise FlowMapperError("Please select the {0}.".format(label))
            if not os.path.isfile(path):
                raise FlowMapperError("The selected {0} does not exist: {1}".format(label, path))
        name_path = values["name_path"]
        if name_path and not os.path.isfile(name_path):
            raise FlowMapperError(
                "The selected node-name file does not exist: {0}".format(name_path)
            )
        if not values["output_path"]:
            raise FlowMapperError("Please select the flow-lines output shapefile.")
        if values["create_nodes"]:
            if not values["node_output_path"]:
                raise FlowMapperError("Please select the flow-nodes output shapefile.")
            if self._shp_path(values["output_path"]) == self._shp_path(
                values["node_output_path"]
            ):
                raise FlowMapperError(
                    "Flow lines and flow nodes must use different output shapefiles."
                )

    def _shp_path(self, output_path):
        path = output_path
        if not path.lower().endswith(".shp"):
            path += ".shp"
        return os.path.normcase(os.path.abspath(path))

    def _confirm_overwrite(self, output_paths):
        existing_paths = []
        for output_path in output_paths:
            path = self._shp_path(output_path)
            if os.path.exists(path):
                existing_paths.append(path)
        if not existing_paths:
            return True
        answer = QtWidgets.QMessageBox.question(
            self.iface.mainWindow(),
            "Replace shapefile(s)?",
            "The following output shapefile(s) already exist. Replace them?\n\n{0}".format(
                "\n".join(existing_paths)
            ),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        return answer == QtWidgets.QMessageBox.Yes

    def generate(self):
        values = self.dialog.values()
        try:
            self._validate_paths(values)
            output_paths = [values["output_path"]]
            if values["create_nodes"]:
                output_paths.append(values["node_output_path"])
            if not self._confirm_overwrite(output_paths):
                self.dialog.status_label.setText("Generation cancelled.")
                return

            self.dialog.set_busy(True)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            node_summary = None
            try:
                summary = create_flow_shapefile(
                    values["coordinate_path"],
                    values["name_path"],
                    values["matrix_path"],
                    values["output_path"],
                    values["flow_type"],
                    epsg=values["epsg"],
                    include_self=values["include_self"],
                    include_zero=values["include_zero"],
                    curved=values["curved"],
                )
                if values["create_nodes"]:
                    try:
                        node_summary = create_node_shapefile(
                            values["coordinate_path"],
                            values["name_path"],
                            values["matrix_path"],
                            values["node_output_path"],
                            epsg=values["epsg"],
                        )
                    except FlowMapperError as exc:
                        raise FlowMapperError(
                            "The flow-lines shapefile was created, but the flow-nodes shapefile failed: {0}".format(
                                text_type(exc)
                            )
                        )
            finally:
                QtWidgets.QApplication.restoreOverrideCursor()
                self.dialog.set_busy(False)

            map_warnings = []
            if values["add_to_map"]:
                layer_name = os.path.splitext(os.path.basename(summary["path"]))[0]
                try:
                    layer = self.iface.addVectorLayer(summary["path"], layer_name, "ogr")
                except Exception:
                    layer = None
                if layer is None or (hasattr(layer, "isValid") and not layer.isValid()):
                    map_warnings.append("QGIS could not add the flow-lines layer to the map.")
                else:
                    presentation_warnings = apply_layer_presentation(
                        layer, summary["flow_type"]
                    )
                    if presentation_warnings:
                        map_warnings.append(
                            "Part of the flow-lines presentation could not be applied: "
                            + "; ".join(presentation_warnings)
                        )

                if node_summary is not None:
                    node_layer_name = os.path.splitext(
                        os.path.basename(node_summary["path"])
                    )[0]
                    try:
                        node_layer = self.iface.addVectorLayer(
                            node_summary["path"], node_layer_name, "ogr"
                        )
                    except Exception:
                        node_layer = None
                    if node_layer is None or (
                        hasattr(node_layer, "isValid") and not node_layer.isValid()
                    ):
                        map_warnings.append(
                            "QGIS could not add the flow-nodes layer to the map."
                        )
                    elif values["color_nodes"]:
                        node_presentation_warnings = apply_node_presentation(
                            node_layer
                        )
                        if node_presentation_warnings:
                            map_warnings.append(
                                "The gain/loss node colors could not be fully applied: "
                                + "; ".join(node_presentation_warnings)
                            )

            message_parts = [
                "FlowMapper created {0} {1} {2} flow lines from {3} nodes.\n{4}".format(
                    summary["feature_count"],
                    summary["line_shape"],
                    summary["flow_type"].replace("_", " "),
                    summary["node_count"],
                    summary["path"],
                )
            ]
            if node_summary is not None:
                message_parts.append(
                    "Created {0} flow nodes.\n{1}".format(
                        node_summary["feature_count"], node_summary["path"]
                    )
                )
            if map_warnings:
                message_parts.append("Map warning(s):\n- " + "\n- ".join(map_warnings))
            message = "\n\n".join(message_parts)

            if node_summary is None:
                status = "Created {0} flow lines.".format(summary["feature_count"])
            else:
                status = "Created {0} flow lines and {1} flow nodes.".format(
                    summary["feature_count"], node_summary["feature_count"]
                )
            self.dialog.status_label.setText(status)
            QtWidgets.QMessageBox.information(
                self.iface.mainWindow(), "FlowMapper", message
            )
        except FlowMapperError as exc:
            if self.dialog is not None:
                self.dialog.set_busy(False)
                self.dialog.status_label.setText("Could not generate the requested outputs.")
            QtWidgets.QMessageBox.warning(
                self.iface.mainWindow(), "FlowMapper", text_type(exc)
            )
        except Exception as exc:
            if self.dialog is not None:
                self.dialog.set_busy(False)
                self.dialog.status_label.setText("Unexpected error.")
            QtWidgets.QMessageBox.critical(
                self.iface.mainWindow(),
                "FlowMapper",
                "Unexpected error: {0}".format(text_type(exc)),
            )
