#!/usr/bin/env python
# coding: utf8
#
# Copyright (c) 2024 Centre National d'Etudes Spatiales (CNES).
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

__author__ = 'CNES'
__date__ = '2023-04-17'
__copyright__ = '(C) 2023 by CNES'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFolderDestination,
                       QgsRasterLayer,
                       QgsProject)

from .import_bulldozer import dsm_to_dtm


class BulldozerDtmProviderAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

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

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Raster'

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)
        #return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return BulldozerDtmProviderAlgorithm()


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), 'bulldozer_logo.png'))


    def tags(self):
        return ['3d', 'bulldozer']


    def shortHelpString(self):
        return self.tr("""Bulldozer is designed as a pipeline of standalone functions that aims to extract a Digital Terrain Model (DTM) from a Digital Surface Model (DSM).
But you can also use one of the following function without running the full pipeline:

DSM preprocessing
- Nodata extraction: a group of methods to differentiate and extract nodata related to failed correlations during the DSM computation and those of the image border
- Disturbed areas detection: a method to locate disturbed areas. These noisy areas are mainly related to areas in which the correlator has incorrectly estimated the elevation (water or shadow areas).


DTM extraction
- DTM computation: the main method that extracts the DTM from the preprocessed DSM.


DTM postprocessing
- Pits detection: a method to detect pits in the provided raster and return the corresponding mask.
- Pits filling: a method to fill pits in the generated DTM (or input raster).
- DHM computation: a method to extract the Digital Height Model (DHM).

For more information about these functions and how to call them, please refer to the notebook documentation section.
https://gitlab.cnes.fr/3d/bulldozer/-/tree/master#notebooks
""")

    def helpUrl(self):  # real signature unknown; restored from __doc__
        """
        helpUrl(self) -> str
        Returns a url pointing to the algorithm's help page.

        .. seealso:: :py:func:`helpString`

        .. seealso:: :py:func:`shortHelpString`
        """
        return "https://gitlab.cnes.fr/3d/bulldozer/-/blob/master/docs/notebooks/0_bulldozer_pipeline.ipynb"