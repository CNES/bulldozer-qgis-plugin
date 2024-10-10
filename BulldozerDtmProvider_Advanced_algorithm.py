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
from qgis.core import (QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingException,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterRasterLayer)

from .import_bulldozer import dsm_to_dtm
from .BulldozerDtmProvider_algorithm import BulldozerDtmProviderAlgorithm
from .BulldozerDtmProvider_Params import (check_params,
                                          get_combined_list_params_for_advanced_app,
                                          BulldozerParameterException)

class BulldozerDtmProviderAdvancedAlgorithm(BulldozerDtmProviderAlgorithm):
    """
    Processing algorithm that calls Bulldozer with advanced parameters.
    """

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def __init__(self):
        super().__init__()
        params = get_combined_list_params_for_advanced_app()
        for param in params:
            setattr(self, param.name.upper(), param.name.upper())

    def initAlgorithm(self, config):
        """
        Define the inputs, output and properties of the algorithm
        """
        params = get_combined_list_params_for_advanced_app()

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            self.tr('Input DSM')
                                                            )
                          )

        for param in params:
            if param.param_type == bool:
                new_param = QgsProcessingParameterBoolean(param.name,
                                                          param.description,
                                                          defaultValue=param.default_value,
                                                          optional=True)
                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

            elif param.param_type == int:
                new_param = QgsProcessingParameterNumber(param.name,
                                                         param.description,
                                                         type=QgsProcessingParameterNumber.Integer,
                                                         minValue=0,
                                                         defaultValue=None,
                                                         optional=True)
                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

            elif param.param_type == float:
                new_param = QgsProcessingParameterNumber(param.name,
                                                         param.description,
                                                         type=QgsProcessingParameterNumber.Double,
                                                         minValue=0,  # FIXME
                                                         defaultValue=None,
                                                         optional=True)

                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

            # elif param.param_type == str:
            #     ## FIXME
            #     self.addParameter(QgsProcessingParameterRasterLayer(param.name,
            #                                                     param.description))


        self.addParameter(QgsProcessingParameterFolderDestination(self.OUTPUT_DIR,
                                                                  self.tr('Output directory'),
                                                                  optional=True))


    def get_params_for_bulldozer(self, parameters, context, feedback):
        """
        Get the parameters for Bulldozer
        """
        params = get_combined_list_params_for_advanced_app()

        params_for_bulldozer = {}

        for param in params:
            param_name = param.name
            param_name_upper = param.name.upper()

            source = self.parameterAsLayer(parameters, self.INPUT, context).source()
            params_for_bulldozer["dsm_path"] = source

            param_value = None
            if param_name in parameters and parameters[param_name] is not None:
                if param.param_type == bool:
                    param_value = self.parameterAsBool(parameters, param_name_upper, context)
                elif param.param_type == int:
                    param_value = self.parameterAsInt(parameters, param_name_upper, context)
                elif param.param_type == float:
                    param_value = self.parameterAsDouble(parameters, param_name_upper, context)
                elif param.param_type == str:
                    param_value = self.parameterAsString(parameters, param_name_upper, context)

                if param_value is not None:
                    params_for_bulldozer[param_name] = param_value

            if "output_dir" not in params_for_bulldozer:
                params_for_bulldozer["output_dir"] = self.parameterAsString(parameters,
                                                                            self.OUTPUT_DIR,
                                                                            context)

        params_for_bulldozer["dsm_path"] = self.parameterAsLayer(parameters,
                                                                 self.INPUT, context).source()

        try:
            check_params(**params_for_bulldozer)
        except BulldozerParameterException as e:
            print(f"#####################{e}####################")
            feedback.reportError(f"Parameters are not valid : {e}", fatalError=True)
            raise QgsProcessingException(f"Parameters are not valid : {e}") from e

        return params_for_bulldozer


    def processAlgorithm(self, parameters, context, feedback):
        """
        Call Bulldozer with full parameters
        """
        params_for_bulldozer = self.get_params_for_bulldozer(parameters, context, feedback)

        dsm_to_dtm(**params_for_bulldozer)

        output_dir = params_for_bulldozer["output_dir"]

        self.OUTPUT = os.path.join(output_dir, "DTM.tif")
        return {self.OUTPUT: os.path.join(output_dir, "DTM.tif")}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'Bulldozer'

    def createInstance(self):
        """
        Create a new instance of the algorithm.
        """
        return BulldozerDtmProviderAdvancedAlgorithm()
