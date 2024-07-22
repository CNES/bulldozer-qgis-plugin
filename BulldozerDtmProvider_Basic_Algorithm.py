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

import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFolderDestination,
                       QgsRasterLayer,
                       QgsProject, QgsProcessingException)

from .import_bulldozer import dsm_to_dtm
from .BulldozerDtmProvider_algorithm import BulldozerDtmProviderAlgorithm
from .BulldozerDtmProvider_Params import check_params, BulldozerParameterException


class BulldozerDtmProviderBasicAlgorithm(BulldozerDtmProviderAlgorithm):
    """
    Processing algorithm that calls Bulldozer with basic parameters.
    """

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    NB_WORKERS = 'NB_WORKERS'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            self.tr('Input DSM')
                                                            )
                          )

        self.addParameter(QgsProcessingParameterNumber(self.NB_WORKERS,
                                                       self.tr('Number max workers'),
                                                       type=QgsProcessingParameterNumber.Integer,
                                                       minValue=0,
                                                       defaultValue=16))

        self.addParameter(QgsProcessingParameterFolderDestination(self.OUTPUT_DIRECTORY,
                                                                  self.tr('Output directory'),
                                                                  optional=True))


    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with basic parameters
        """

        source = self.parameterAsLayer(parameters, self.INPUT, context).source()
        nb_max_workers = self.parameterAsInt(parameters, self.NB_WORKERS, context)

        output_dir = self.parameterAsString(parameters, self.OUTPUT_DIRECTORY, context)

        try:
            check_params(dsm_path=source, output_dir=output_dir, nb_max_workers=nb_max_workers)
        except BulldozerParameterException as e:
            feedback.reportError(f"Parameters are not valid : {e}", fatalError=True)
            raise QgsProcessingException(f"Parameters are not valid : {e}")

        dsm_to_dtm(dsm_path=source, output_dir=output_dir, nb_max_workers=nb_max_workers)

        self.OUTPUT = os.path.join(output_dir, "DTM.tif")
        return {self.OUTPUT: os.path.join(output_dir, "DTM.tif")}

    def postProcessAlgorithm(self, context, feedback):
        """
        Add the DTM to the map
        """
        rlayer = QgsRasterLayer(self.OUTPUT, "DTM")

        if not rlayer.isValid():
            print("Layer failed to load!")

        QgsProject.instance().addMapLayer(rlayer)

        return {self.OUTPUT: self.OUTPUT}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'Bulldozer (Basic)'

    def createInstance(self):
        """
        Create a new instance of the algorithm.
        """
        return BulldozerDtmProviderBasicAlgorithm()
