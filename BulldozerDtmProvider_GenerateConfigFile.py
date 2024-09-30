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
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterFileDestination,
                       QgsRasterLayer,
                       QgsProject, QgsProcessingException)

from .BulldozerDtmProvider_algorithm import BulldozerDtmProviderAlgorithm
from .BulldozerDtmProvider_Params import (check_params,
                                          get_combined_list_params_for_advanced_app,
                                          BulldozerParameterException)


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
    OUTPUT_DIR = 'OUTPUT_DIR'
    CONFIG_FILE = 'CONFIG_FILE'

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """

        self.addParameter(QgsProcessingParameterFileDestination(self.CONFIG_FILE,
                                                                self.tr('Config file'),
                                                                fileFilter='YAML files (*.yaml)')
                          )

        params = get_combined_list_params_for_advanced_app()


        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            self.tr('Input DSM')
                                                            )
                          )

        for param in params:
            if param.param_type == bool:
                self.addParameter(QgsProcessingParameterBoolean(param.name,
                                                                param.description,
                                                                defaultValue=param.default_value))

            elif param.param_type == int:
                self.addParameter(QgsProcessingParameterNumber(param.name,
                                                            param.description,
                                                            type=QgsProcessingParameterNumber.Integer,
                                                            minValue=0,  # FIXME
                                                            defaultValue=param.default_value))

            elif param.param_type == float:
                self.addParameter(QgsProcessingParameterNumber(param.name,
                                                            param.description,
                                                            type=QgsProcessingParameterNumber.Double,
                                                            minValue=0,  # FIXME
                                                            defaultValue=param.default_value))

            # elif param.param_type == str:
            #     ## FIXME
            #     self.addParameter(QgsProcessingParameterRasterLayer(param.name,
            #                                                     param.description))

        self.addParameter(QgsProcessingParameterFolderDestination(self.OUTPUT_DIR,
                                                                  self.tr('Output directory'),
                                                                  optional=True))


    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with full parameters
        """

        params = get_combined_list_params_for_advanced_app()

        params_for_bulldozer = {}

        for param in params:
            print(param)
            param_name = param.name
            param_name_upper = param.name.upper()

            if param.param_type == bool:
                param_value = self.parameterAsBool(parameters, param_name_upper, context)
            elif param.param_type == int:
                param_value = self.parameterAsInt(parameters, param_name_upper, context)
                if param.default_value is None:
                    if param_value == 0:
                        param_value = None
            elif param.param_type == float:
                param_value = self.parameterAsDouble(parameters, param_name_upper, context)
                if param.default_value is None:
                    if param_value == 0.0:
                        param_value = None
            elif param.param_type == str:
                param_value = self.parameterAsString(parameters, param_name_upper, context)

            params_for_bulldozer[param_name] = param_value

        params_for_bulldozer["dsm_path"] = self.parameterAsLayer(parameters,
                                                                 self.INPUT, context).source()
        params_for_bulldozer["config_file"] = self.parameterAsString(parameters,
                                                                     self.CONFIG_FILE, context)

        try:
            check_params(**params_for_bulldozer)
        except BulldozerParameterException as e:
            print(f"#####################{e}####################")
            feedback.reportError(f"Parameters are not valid : {e}", fatalError=True)
            raise QgsProcessingException(f"Parameters are not valid : {e}")


        with open(params_for_bulldozer["config_file"], 'w') as f:
            for key, value in params_for_bulldozer.items():
                if value is not None:
                    f.write(f"{key}: {value} \n")

            # f.write(f"dsm_path: {source} \n")
            # f.write(f"output_dir: {output_dir} \n")
            # f.write(f"nb_max_workers: {nb_max_workers} \n")
            # f.write(f"generate_dhm: {generate_dhm} \n")
            # f.write(f"max_object_width: {max_object_width} \n")
            # f.write(f"output_resolution: {output_resolution} \n")
            # f.write(f"no_data: {no_data} \n")
            # f.write(f"min_valid_heigh: {min_valid_heigh} \n")
            # f.write(f"check_intersection: {check_intersection} \n")
            # f.write(f"developper_mode: {developper_mode} \n")
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
