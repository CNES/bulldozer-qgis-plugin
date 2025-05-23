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


class BulldozerDtmProviderSettings:
    """
    Setting's key names
    """
    # Checkbox to enable/disable bulldozer provider (bool).
    ACTIVATE = "BULLDOZER_ACTIVATE"

    @staticmethod
    def keys():
        """ Return the list of settings defined in this class """
        return [
            BulldozerDtmProviderSettings.ACTIVATE
        ]
