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
__date__ = '2023-05-24'
__copyright__ = '(C) 2023 by CNES'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterFileDestination,
                       QgsRasterLayer,
                       QgsProject)

from .import_bulldozer import dsm_to_dtm
from .BulldozerDtmProvider_algorithm import BulldozerDtmProviderAlgorithm

class BulldozerDtmProviderGenerateConfigFile(BulldozerDtmProviderAlgorithm):
    """
    Processing algorithm that generates config file with advanced parameters.
    """

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    NB_WORKERS = 'NB_WORKERS'
    GENERATE_DHM = 'GENERATE_DHM'
    MAX_OBJECT_WIDTH = 'MAX_OBJECT_WIDTH'
    OUTPUT_RES = 'OUTPUT_RES'
    NO_DATA = 'NO_DATA'
    MIN_VALID_HEIGH = 'MIN_VALID_HEIGH'
    CHECK_INTERSECTION = 'CHECK_INTERSECTION'
    DEVELOPPER_MODE = 'DEVELOPPER_MODE'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'
    CONFIG_FILE = 'CONFIG_FILE'

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """
        self.addParameter(QgsProcessingParameterFileDestination(self.CONFIG_FILE,
                                                                  self.tr('Config file'),
                                                                  optional=True))


        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            self.tr('Input DSM')
                                                            )
                          )

        self.addParameter(QgsProcessingParameterNumber(self.NB_WORKERS,
                                                       self.tr('Number max workers'),
                                                       type=QgsProcessingParameterNumber.Integer,
                                                       minValue=0,
                                                       defaultValue=16))

        self.addParameter(QgsProcessingParameterBoolean(self.GENERATE_DHM,
                                                        self.tr('Generates the DHM (DSM - DTM)'),
                                                        defaultValue=False))

        self.addParameter(QgsProcessingParameterNumber(self.MAX_OBJECT_WIDTH,
                                                       self.tr('Foreground max object width '
                                                               '(in meter)'),
                                                       type=QgsProcessingParameterNumber.Integer,
                                                       minValue=0,
                                                       defaultValue=16))

        self.addParameter(QgsProcessingParameterNumber(self.OUTPUT_RES,
                                                       self.tr('Output DTM resolution'),
                                                       type=QgsProcessingParameterNumber.Double,
                                                       minValue=0))

        self.addParameter(QgsProcessingParameterNumber(self.NO_DATA,
                                                       self.tr('Nodata value of the input DSM'),
                                                       type=QgsProcessingParameterNumber.Double))

        self.addParameter(QgsProcessingParameterNumber(self.MIN_VALID_HEIGH,
                                                       self.tr(
                                                           'DSM minimum valid elevation. All the '
                                                           'points lower this threshold will be '
                                                           'consider as nodata'),
                                                       type=QgsProcessingParameterNumber.Double))

        self.addParameter(QgsProcessingParameterBoolean(self.CHECK_INTERSECTION,
                                                        self.tr('Allows snapping DTM values above '
                                                                'the DSM to the DSM'),
                                                        defaultValue=False))

        self.addParameter(QgsProcessingParameterBoolean(self.DEVELOPPER_MODE,
                                                        self.tr('Keep the intermediate results'),
                                                        defaultValue=False))

        self.addParameter(QgsProcessingParameterFolderDestination(self.OUTPUT_DIRECTORY,
                                                                  self.tr('Bulldozer output '
                                                                          'directory'),
                                                                  optional=True))


    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with full parameters
        """

        source = self.parameterAsLayer(parameters, self.INPUT, context).source()
        nb_max_workers = self.parameterAsInt(parameters, self.NB_WORKERS, context)
        generate_dhm = self.parameterAsInt(parameters, self.GENERATE_DHM, context)
        max_object_width = self.parameterAsInt(parameters, self.MAX_OBJECT_WIDTH, context)
        output_resolution = self.parameterAsInt(parameters, self.OUTPUT_RES, context)
        no_data = self.parameterAsInt(parameters, self.NO_DATA, context)
        min_valid_heigh = self.parameterAsInt(parameters, self.MIN_VALID_HEIGH, context)
        check_intersection = self.parameterAsInt(parameters, self.CHECK_INTERSECTION, context)
        developper_mode = self.parameterAsInt(parameters, self.DEVELOPPER_MODE, context)
        output_dir = self.parameterAsString(parameters, self.OUTPUT_DIRECTORY, context)
        config_file = self.parameterAsString(parameters, self.CONFIG_FILE, context)

        with open(config_file, 'w') as f:
            f.write(f"dsm_path: {source} \n")
            f.write(f"output_dir: {output_dir} \n")
            f.write(f"nb_max_workers: {nb_max_workers} \n")
            f.write(f"generate_dhm: {generate_dhm} \n")
            f.write(f"max_object_width: {max_object_width} \n")
            f.write(f"output_resolution: {output_resolution} \n")
            f.write(f"no_data: {no_data} \n")
            f.write(f"min_valid_heigh: {min_valid_heigh} \n")
            f.write(f"check_intersection: {check_intersection} \n")
            f.write(f"developper_mode: {developper_mode} \n")

        return {self.OUTPUT: config_file}

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
        return 'Bulldozer (Generate config file)'

    def createInstance(self):
        """
        Create a new instance of the algorithm.
        """
        return BulldozerDtmProviderGenerateConfigFile()
