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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessingAlgorithm,
                       QgsRasterLayer,
                       QgsProject)

# Initialize Qt resources from file resources.py
from .resources import *


class BulldozerDtmProviderAlgorithm(QgsProcessingAlgorithm):
    """
    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)
        #return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return BulldozerDtmProviderAlgorithm()


    def icon(self):
        return QIcon(':/plugins/bulldozerdtmprovider/img/bulldozer_logo.png')

    def tags(self):
        return ['3d', 'bulldozer']


    def shortHelpString(self):
        return self.tr("""Bulldozer is a pipeline designed to extract a Digital Terrain Model (DTM) from a Digital Surface Model (DSM). It supports both noisy satellite DSMs and high-quality LiDAR DSMs. It relies on a morphological approach.

Bulldozer is licensed under Apache License v2.0.

You can find more information in the documentation: https://bulldozer.readthedocs.io/

If you want to contribute or report an issue in the plugin, here is the repository link: https://github.com/CNES/bulldozer-qgis-plugin
""")

    def helpUrl(self):  # real signature unknown; restored from __doc__
        """
        helpUrl(self) -> str
        Returns a url pointing to the algorithm's help page.

        .. seealso:: :py:func:`helpString`

        .. seealso:: :py:func:`shortHelpString`
        """
        return "https://bulldozer.readthedocs.io/"

    def postProcessAlgorithm(self, context, feedback):
        """
        Add the DTM to the map
        """
        rlayer = QgsRasterLayer(self.OUTPUT, "DTM")

        if not rlayer.isValid():
            print("Layer failed to load!")

        QgsProject.instance().addMapLayer(rlayer)

        return {self.OUTPUT: self.OUTPUT}
