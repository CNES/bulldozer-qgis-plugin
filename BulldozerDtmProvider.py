#!/usr/bin/env python
# coding: utf8
#
# Copyright (c) 2023-2025 Centre National d'Etudes Spatiales (CNES).
#
# This file is part of Bulldozer
# (see https://github.com/CNES/bulldozer-qgis-plugin).
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html for
# more details.


import os
import sys
import inspect

from qgis.core import QgsApplication
from .BulldozerDtmProvider_provider import BulldozerDtmProviderProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class BulldozerDtmProviderPlugin:
    """ Bulldozer DTM Provider Plugin Definition """

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = BulldozerDtmProviderProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """ Init the plugin interface """
        self.initProcessing()

    def unload(self):
        """ Unload the plugin """
        QgsApplication.processingRegistry().removeProvider(self.provider)
