# -*- coding: utf-8 -*-
"""Small PyQt compatibility layer shared by QGIS 2 and QGIS 3."""

from __future__ import absolute_import

try:
    # QGIS 3: Qt is exposed through the stable qgis.PyQt namespace.
    from qgis.PyQt import QtCore, QtGui, QtWidgets
    QGIS3 = True
except ImportError:
    # QGIS 2: widgets are part of PyQt4.QtGui.
    from PyQt4 import QtCore, QtGui
    QtWidgets = QtGui
    QGIS3 = False


try:
    text_type = unicode
except NameError:
    text_type = str


def dialog_path(value):
    """Normalize QFileDialog results from PyQt4 and PyQt5."""
    if isinstance(value, (tuple, list)):
        value = value[0]
    return text_type(value)


def exec_dialog(dialog):
    """Run a modal dialog across PyQt4, PyQt5 and PyQt6 APIs."""
    execute = getattr(dialog, "exec", None)
    if execute is None:
        execute = getattr(dialog, "exec_")
    return execute()


__all__ = (
    "QGIS3",
    "QtCore",
    "QtGui",
    "QtWidgets",
    "dialog_path",
    "exec_dialog",
    "text_type",
)
