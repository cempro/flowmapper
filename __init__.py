# -*- coding: utf-8 -*-
"""QGIS entry point for FlowMapper."""

from __future__ import absolute_import


def classFactory(iface):
    """Return the plugin instance expected by QGIS 2 and QGIS 3."""
    from .flowmapper import FlowMapper
    return FlowMapper(iface)
