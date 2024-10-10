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


from qgis.core import QgsProcessingParameterFileDestination

from .BulldozerDtmProvider_Advanced_algorithm import BulldozerDtmProviderAdvancedAlgorithm


class BulldozerDtmProviderGenerateConfigFile(BulldozerDtmProviderAdvancedAlgorithm):
    """
    Processing algorithm that generates config file with advanced parameters.
    """

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    CONFIG_FILE = 'CONFIG_FILE'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """

        super().initAlgorithm(config)

        self.addParameter(QgsProcessingParameterFileDestination(self.CONFIG_FILE,
                                                                self.tr('Config file'),
                                                                fileFilter='YAML files (*.yaml)')
                          )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with full parameters
        """
        params_for_bulldozer = self.get_params_for_bulldozer(parameters, context, feedback)

        params_for_bulldozer["config_file"] = self.parameterAsString(parameters,
                                                                     self.CONFIG_FILE, context)

        with open(params_for_bulldozer["config_file"], 'w') as f:
            for key, value in params_for_bulldozer.items():
                if value is not None:
                    f.write(f"{key}: {value} \n")

        self.OUTPUT = params_for_bulldozer["config_file"]
        return {self.OUTPUT: params_for_bulldozer["config_file"]}

    def postProcessAlgorithm(self, context, feedback):
        """
        Add the DTM to the map
        """
        feedback.pushInfo("Config file : " + self.OUTPUT)

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
