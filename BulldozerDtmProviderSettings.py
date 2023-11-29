# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'CNES'
__date__ = '2023-04-12'
__copyright__ = '(C) 2023 by CNES'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'


class BulldozerDtmProviderSettings(object):
    """
    OtbSetting's key names
    """
    # Checkbox to enable/disable otb provider (bool).
    ACTIVATE = "BULLDOZER_ACTIVATE"

    # Path to otb installation folder (string, directory).
    FOLDER = "BULLDOZER_FOLDER"

    @staticmethod
    def keys():
        return [
            BulldozerDtmProviderSettings.ACTIVATE,
            BulldozerDtmProviderSettings.FOLDER,
        ]

