# -*- coding: utf-8 -*-
"""FlowMapper dialogs, built in code for PyQt4/PyQt5 portability."""

from __future__ import absolute_import, unicode_literals

import os

from .qt_compat import QtCore, QtGui, QtWidgets, dialog_path, text_type


class FlowMapperDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("FlowMapper")
        self.setMinimumWidth(720)
        self._build_ui()

    def _path_row(
        self,
        placeholder,
        save=False,
        save_title="Save output shapefile",
        default_name="flow_lines.shp",
    ):
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        line_edit = QtWidgets.QLineEdit(widget)
        if hasattr(line_edit, "setPlaceholderText"):
            line_edit.setPlaceholderText(placeholder)
        button = QtWidgets.QPushButton("Browse...", widget)
        layout.addWidget(line_edit, 1)
        layout.addWidget(button)
        if save:
            button.clicked.connect(
                lambda: self._browse_output(line_edit, save_title, default_name)
            )
        else:
            button.clicked.connect(lambda: self._browse_input(line_edit))
        return widget, line_edit

    def _build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        intro = QtWidgets.QLabel(
            "Create flow lines and optional node summaries from coordinates, optional names and a square origin-destination matrix.",
            self,
        )
        intro.setWordWrap(True)
        main_layout.addWidget(intro)

        input_group = QtWidgets.QGroupBox("Input text files", self)
        input_layout = QtWidgets.QFormLayout(input_group)

        coordinate_widget, self.coordinate_edit = self._path_row("X Y coordinates (.txt)")
        name_widget, self.name_edit = self._path_row(
            "Optional: one node name per line (.txt)"
        )
        matrix_widget, self.matrix_edit = self._path_row("N x N flow matrix (.txt)")
        input_layout.addRow("Node coordinates:", coordinate_widget)
        input_layout.addRow("Node names (optional):", name_widget)
        input_layout.addRow("Flow matrix:", matrix_widget)

        crs_widget = QtWidgets.QWidget(self)
        crs_layout = QtWidgets.QHBoxLayout(crs_widget)
        crs_layout.setContentsMargins(0, 0, 0, 0)
        self.crs_combo = QtWidgets.QComboBox(crs_widget)
        self.crs_combo.addItem("Geographic (EPSG:4326)")
        self.crs_combo.addItem("Other EPSG code")
        self.epsg_label = QtWidgets.QLabel("EPSG:", crs_widget)
        self.epsg_spin = QtWidgets.QSpinBox(crs_widget)
        self.epsg_spin.setRange(1, 999999)
        self.epsg_spin.setValue(4326)
        crs_layout.addWidget(self.crs_combo, 1)
        crs_layout.addWidget(self.epsg_label)
        crs_layout.addWidget(self.epsg_spin)
        input_layout.addRow("Coordinate reference system:", crs_widget)
        main_layout.addWidget(input_group)

        flow_group = QtWidgets.QGroupBox("Flow type", self)
        flow_layout = QtWidgets.QVBoxLayout(flow_group)
        radio_layout = QtWidgets.QHBoxLayout()
        self.two_way_radio = QtWidgets.QRadioButton("Two-way", flow_group)
        self.gross_radio = QtWidgets.QRadioButton("Gross", flow_group)
        self.net_radio = QtWidgets.QRadioButton("Net", flow_group)
        self.net_radio.setChecked(True)
        radio_layout.addWidget(self.two_way_radio)
        radio_layout.addWidget(self.gross_radio)
        radio_layout.addWidget(self.net_radio)
        radio_layout.addStretch(1)
        flow_layout.addLayout(radio_layout)
        self.flow_explanation = QtWidgets.QLabel(flow_group)
        self.flow_explanation.setWordWrap(True)
        flow_layout.addWidget(self.flow_explanation)
        main_layout.addWidget(flow_group)

        output_group = QtWidgets.QGroupBox("Output", self)
        output_layout = QtWidgets.QFormLayout(output_group)
        output_widget, self.output_edit = self._path_row(
            "Output flow-lines shapefile (.shp)",
            save=True,
            save_title="Save flow lines",
            default_name="flow_lines.shp",
        )
        output_layout.addRow("Flow lines:", output_widget)
        line_shape_widget = QtWidgets.QWidget(output_group)
        line_shape_layout = QtWidgets.QHBoxLayout(line_shape_widget)
        line_shape_layout.setContentsMargins(0, 0, 0, 0)
        self.straight_line_radio = QtWidgets.QRadioButton(
            "Generate straight flow lines", line_shape_widget
        )
        self.curved_line_radio = QtWidgets.QRadioButton(
            "Generate curved flow lines", line_shape_widget
        )
        self.straight_line_radio.setChecked(True)
        line_shape_layout.addWidget(self.straight_line_radio)
        line_shape_layout.addWidget(self.curved_line_radio)
        line_shape_layout.addStretch(1)
        output_layout.addRow(line_shape_widget)
        self.create_nodes_check = QtWidgets.QCheckBox("Create flow nodes", output_group)
        self.create_nodes_check.setChecked(False)
        self.create_nodes_check.setToolTip(
            "Create a point shapefile with outgoing, incoming and signed net totals."
        )
        output_layout.addRow(self.create_nodes_check)
        self.node_output_widget, self.node_output_edit = self._path_row(
            "Output flow-nodes shapefile (.shp)",
            save=True,
            save_title="Save flow nodes",
            default_name="flow_nodes.shp",
        )
        self.node_output_label = QtWidgets.QLabel("Flow nodes:", output_group)
        output_layout.addRow(self.node_output_label, self.node_output_widget)
        self.color_nodes_check = QtWidgets.QCheckBox(
            "Color nodes by flow gain/loss", output_group
        )
        self.color_nodes_check.setChecked(False)
        self.color_nodes_check.setToolTip(
            "Gain (incoming > outgoing): green; Loss (outgoing > incoming): red; Balanced: gray."
        )
        output_layout.addRow(self.color_nodes_check)
        main_layout.addWidget(output_group)

        option_layout = QtWidgets.QHBoxLayout()
        self.skip_zero_check = QtWidgets.QCheckBox("Skip zero-magnitude flows", self)
        self.skip_zero_check.setChecked(True)
        self.self_flow_check = QtWidgets.QCheckBox(
            "Include inner flows (diagonal, zero-length)", self
        )
        self.self_flow_check.setChecked(False)
        self.self_flow_check.setToolTip(
            "Inner flows are diagonal matrix values and produce zero-length lines."
        )
        self.add_map_check = QtWidgets.QCheckBox("Add result to map", self)
        self.add_map_check.setChecked(True)
        option_layout.addWidget(self.skip_zero_check)
        option_layout.addWidget(self.self_flow_check)
        option_layout.addWidget(self.add_map_check)
        option_layout.addStretch(1)
        main_layout.addLayout(option_layout)

        self.status_label = QtWidgets.QLabel("Ready.", self)
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.about_button = self.button_box.addButton("About", QtWidgets.QDialogButtonBox.HelpRole)
        self.generate_button = self.button_box.addButton("Generate", QtWidgets.QDialogButtonBox.AcceptRole)
        self.close_button = self.button_box.addButton(QtWidgets.QDialogButtonBox.Close)
        self.close_button.clicked.connect(self.reject)
        main_layout.addWidget(self.button_box)

        self.crs_combo.currentIndexChanged.connect(self._update_crs_controls)
        self.two_way_radio.toggled.connect(self._update_flow_explanation)
        self.gross_radio.toggled.connect(self._update_flow_explanation)
        self.net_radio.toggled.connect(self._update_flow_explanation)
        self.create_nodes_check.toggled.connect(self._update_node_output_controls)
        self._update_crs_controls()
        self._update_flow_explanation()
        self._update_node_output_controls()

    def _browse_input(self, line_edit):
        current = text_type(line_edit.text()).strip()
        start = os.path.dirname(current) if current else ""
        selected = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select text file", start, "Text files (*.txt);;All files (*)"
        )
        selected = dialog_path(selected)
        if selected:
            line_edit.setText(selected)

    def _browse_output(self, line_edit, title, default_name):
        current = text_type(line_edit.text()).strip()
        start = current if current else default_name
        selected = QtWidgets.QFileDialog.getSaveFileName(
            self, title, start, "ESRI Shapefile (*.shp)"
        )
        selected = dialog_path(selected)
        if selected and not selected.lower().endswith(".shp"):
            selected += ".shp"
        if selected:
            line_edit.setText(selected)

    def _update_crs_controls(self, *unused):
        is_default = self.crs_combo.currentIndex() == 0
        if is_default:
            self.epsg_spin.setValue(4326)
        self.epsg_spin.setEnabled(not is_default)
        self.epsg_label.setEnabled(not is_default)

    def _update_flow_explanation(self, *unused):
        explanations = {
            "two_way": "Two-way: Creates a separate flow line for each direction.",
            "gross": "Gross: Combines flows in both directions for each pair of nodes.",
            "net": "Net: Shows the difference between opposing flows in the direction of the larger flow.",
        }
        self.flow_explanation.setText(explanations[self.flow_type()])

    def _update_node_output_controls(self, *unused):
        enabled = self.create_nodes_check.isChecked()
        self.node_output_label.setEnabled(enabled)
        self.node_output_widget.setEnabled(enabled)
        self.color_nodes_check.setEnabled(enabled)

    def flow_type(self):
        if self.two_way_radio.isChecked():
            return "two_way"
        if self.gross_radio.isChecked():
            return "gross"
        return "net"

    def values(self):
        return {
            "coordinate_path": text_type(self.coordinate_edit.text()).strip(),
            "name_path": text_type(self.name_edit.text()).strip(),
            "matrix_path": text_type(self.matrix_edit.text()).strip(),
            "output_path": text_type(self.output_edit.text()).strip(),
            "curved": self.curved_line_radio.isChecked(),
            "create_nodes": self.create_nodes_check.isChecked(),
            "node_output_path": text_type(self.node_output_edit.text()).strip(),
            "color_nodes": (
                self.create_nodes_check.isChecked()
                and self.color_nodes_check.isChecked()
            ),
            "flow_type": self.flow_type(),
            "epsg": int(self.epsg_spin.value()),
            "include_zero": not self.skip_zero_check.isChecked(),
            "include_self": self.self_flow_check.isChecked(),
            "add_to_map": self.add_map_check.isChecked(),
        }

    def set_busy(self, busy):
        self.generate_button.setEnabled(not busy)
        if busy:
            self.status_label.setText("Generating output shapefiles...")
        QtWidgets.QApplication.processEvents()


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("About FlowMapper")
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(os.path.dirname(__file__), "about.png"))
        )
        self.setMinimumSize(540, 380)
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("<h2>FlowMapper 1.0.0</h2>", self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        browser = QtWidgets.QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            "<p><b>QGIS 2.x / QGIS 3.x compatible flow-line generator</b></p>"
            "<p>Creates straight or curved Two-way, Gross and Net flow lines and an optional node-point "
            "summary from a square origin-destination matrix and corresponding node "
            "coordinates/optional names.</p>"
            "<ul>"
            "<li><b>Two-way:</b> preserves every directed matrix value.</li>"
            "<li><b>Gross:</b> sums both directions for each node pair.</li>"
            "<li><b>Net:</b> stores the absolute difference and draws toward the dominant direction.</li>"
            "</ul>"
            "<p>Original FlowMapper concept and development: <b>Cem GULLUOGLU</b><br>"
            "Inspired by Alan Glennon&rsquo;s FlowpyGIS<br>"
            "Contact: <a href='mailto:cempro@gmail.com'>cempro@gmail.com</a><br>"
            "Repository: <a href='https://github.com/cempro/flowmapper'>github.com/cempro/flowmapper</a></p>"
            "<p>This cross-version release focuses on the core generation module of "
            "FlowMapper version 0.4.1.</p>"
        )
        layout.addWidget(browser, 1)
        buttons = QtWidgets.QDialogButtonBox(self)
        buttons.addButton(QtWidgets.QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
