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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingParameterFile,
                       QgsProcessingException)

from bulldozer.utils.config_parser import ConfigParser
from .import_bulldozer import dsm_to_dtm
#TODO: remove suppress_stdout_if_none and suppress_stderr_if_none imports when tqdm bug on windows gui is fixed
from .BulldozerDtmProvider_algorithm import BulldozerDtmProviderAlgorithm, suppress_stdout_if_none, suppress_stderr_if_none
from .BulldozerDtmProvider_Params import check_params, BulldozerParameterException

class BulldozerDtmProviderConfigFileAlgorithm(BulldozerDtmProviderAlgorithm):
    """
    Processing algorithm that calls Bulldozer with config file.
    """

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """

        self.addParameter(QgsProcessingParameterFile(self.INPUT,
                                                     self.tr('Input YAML config file'),
                                                     extension="yaml"
                                                     )
                          )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with config file
        """

        source = self.parameterAsString(parameters, self.INPUT, context)

        with suppress_stdout_if_none(), suppress_stderr_if_none():
            dsm_to_dtm(config_path=source)

        parser = ConfigParser(False)
        input_params = parser.read(source)
        output_dir=input_params['output_dir']

        self.OUTPUT = os.path.join(output_dir, "dtm.tif")
        return {self.OUTPUT: os.path.join(output_dir, "dtm.tif")}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'Bulldozer (Using config file)'

    def createInstance(self):
        """
        Create a new instance of the algorithm.
        """
        return BulldozerDtmProviderConfigFileAlgorithm()
