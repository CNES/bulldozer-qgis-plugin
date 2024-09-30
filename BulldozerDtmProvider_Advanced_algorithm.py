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
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFolderDestination,
                       QgsRasterLayer,
                       QgsProject, QgsProcessingException,
                       QgsProcessingParameterDefinition)

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
    NB_WORKERS = 'NB_WORKERS'
    GENERATE_DHM = 'GENERATE_DHM'
    MAX_OBJECT_WIDTH = 'MAX_OBJECT_WIDTH'
    OUTPUT_RES = 'OUTPUT_RES'
    NO_DATA = 'NO_DATA'
    MIN_VALID_HEIGH = 'MIN_VALID_HEIGH'
    CHECK_INTERSECTION = 'CHECK_INTERSECTION'
    DEVELOPPER_MODE = 'DEVELOPPER_MODE'
    OUTPUT_DIR = 'OUTPUT_DIR'

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
                                                          defaultValue=param.default_value)
                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

            elif param.param_type == int:
                new_param = QgsProcessingParameterNumber(param.name,
                                                         param.description,
                                                         type=QgsProcessingParameterNumber.Integer,
                                                         minValue=0,  # FIXME
                                                         defaultValue=param.default_value)
                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

            elif param.param_type == float:
                new_param = QgsProcessingParameterNumber(param.name,
                                                         param.description,
                                                         type=QgsProcessingParameterNumber.Double,
                                                         minValue=0,  # FIXME
                                                         defaultValue=param.default_value)

                new_param.setFlags(new_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
                self.addParameter(new_param)

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

        # for param in params:

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
        # params_for_bulldozer["output_dir"] = self.parameterAsString(parameters,
        # self.OUTPUT_DIRECTORY, context)

        # source = self.parameterAsLayer(parameters, self.INPUT, context).source()
        # nb_max_workers = self.parameterAsInt(parameters, self.NB_WORKERS, context)
        # generate_dhm = self.parameterAsInt(parameters, self.GENERATE_DHM, context)
        # max_object_width = self.parameterAsInt(parameters, self.MAX_OBJECT_WIDTH, context)
        # output_resolution = self.parameterAsInt(parameters, self.OUTPUT_RES, context)
        # no_data = self.parameterAsInt(parameters, self.NO_DATA, context)
        # min_valid_height = self.parameterAsInt(parameters, self.MIN_VALID_HEIGH, context)
        # check_intersection = self.parameterAsInt(parameters, self.CHECK_INTERSECTION, context)
        # developper_mode = self.parameterAsInt(parameters, self.DEVELOPPER_MODE, context)
        # output_dir = self.parameterAsString(parameters, self.OUTPUT_DIRECTORY, context)

        try:
            # check_params(dsm_path=source, output_dir=output_dir, nb_max_workers=nb_max_workers,
            #        generate_dhm=generate_dhm, max_object_width=max_object_width,
            #        output_resolution=output_resolution, no_data=no_data,
            #        min_valid_height=min_valid_height, check_intersection=check_intersection,
            #        developper_mode=developper_mode)
            check_params(**params_for_bulldozer)
        except BulldozerParameterException as e:
            print(f"#####################{e}####################")
            feedback.reportError(f"Parameters are not valid : {e}", fatalError=True)
            raise QgsProcessingException(f"Parameters are not valid : {e}")

        # dsm_to_dtm(dsm_path=source, output_dir=output_dir, nb_max_workers=nb_max_workers,
        #            generate_dhm=generate_dhm, max_object_width=max_object_width,
        #            output_resolution=output_resolution, no_data=no_data,
        #            min_valid_height=min_valid_height, check_intersection=check_intersection,
        #            developper_mode=developper_mode)
        dsm_to_dtm(**params_for_bulldozer)

        output_dir = params_for_bulldozer["output_dir"]

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
        return 'Bulldozer (Advanced)'

    def createInstance(self):
        """
        Create a new instance of the algorithm.
        """
        return BulldozerDtmProviderAdvancedAlgorithm()
