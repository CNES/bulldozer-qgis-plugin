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

from .bulldozer_parameters import bulldozer_pipeline_params


class BulldozerParameterException(Exception):
    """ Custom exception for Bulldozer parameters
    """


def get_combined_list_params():
    """ Combine all the parameters from the different algorithms
    """
    params = []

    for ll in bulldozer_pipeline_params.values():
        params.extend(ll)

    return params



def get_combined_list_params_for_advanced_app():
    """ Combine all the parameters from the different algorithms
    """
    params = bulldozer_pipeline_params["REQUIRED (if no config file)"] + \
        bulldozer_pipeline_params["BASIC SETTINGS"] + \
        bulldozer_pipeline_params["ADVANCED SETTINGS"]

    return params


def get_from_params_base(param_name, list_param_objects):
    """ Get the value of a parameter from the parameters dictionary
    """
    res_temp = [param for param in list_param_objects if param.name == param_name]
    if len(res_temp) == 1:
        return res_temp[0]
    elif len(res_temp) == 0:
        message = f"Parameter not found in the parameters dictionary:{param_name}"
        raise BulldozerParameterException(message)
    else:
        raise BulldozerParameterException("Multiple parameters found in the parameters dictionary")



def check_params(*args, **kwargs):
    """ Check given parameters
    """

    print("*******************")
    print("Check params")
    print(args)
    print(kwargs)

    params_baseline = get_combined_list_params()

    # pour chaque parametre de la fonction, récuprérer le paramètre correspondant
    # avec get_from_params_base
    for key, value in kwargs.items():
        if key == "config_file":
            if not isinstance(value, str):
                raise BulldozerParameterException(f"Parameter {key} should be a string")
            continue
        print(key, value)
        param_obj = get_from_params_base(key, params_baseline)

        if param_obj.param_type == str:
            if not isinstance(value, str):
                raise BulldozerParameterException(f"Parameter {key} should be a string")
        elif param_obj.param_type == int:
            if value == param_obj.default_value:
                continue
            if not isinstance(value, int):
                raise BulldozerParameterException(f"Parameter {key} should be an integer")
        elif param_obj.param_type == float:
            if value == param_obj.default_value:
                continue
            if not isinstance(value, float):
                try:
                    float(value)
                except ValueError:
                    raise BulldozerParameterException(f"Parameter {key} should be a float")
        elif param_obj.param_type == bool:
            if not isinstance(value, bool):
                try:
                    bool(value)
                except ValueError:
                    raise BulldozerParameterException(f"Parameter {key} should be a boolean")
        else:
            raise BulldozerParameterException(f"Parameter {key} has an unknown type")

        if key == "output_dir":
            if "processing_" in value:
                continue
            elif not os.path.isdir(value):
                raise BulldozerParameterException(f"Output directory {value} does not exist")

        if key == "dsm_path":
            if not os.path.isfile(value):
                raise BulldozerParameterException(f"DSM file {value} does not exist")

    print("*******************")
