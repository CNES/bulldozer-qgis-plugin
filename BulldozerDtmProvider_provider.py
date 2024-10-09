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

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from processing.core.ProcessingConfig import (ProcessingConfig, Setting)

from .BulldozerDtmProvider_Advanced_algorithm import BulldozerDtmProviderAdvancedAlgorithm
from .BulldozerDtmProviderSettings import BulldozerDtmProviderSettings
from .BulldozerDtmProvider_ConfigFile_algorithm import BulldozerDtmProviderConfigFileAlgorithm
from .BulldozerDtmProvider_GenerateConfigFile import BulldozerDtmProviderGenerateConfigFile

# Initialize Qt resources from file resources.py
from .resources import *


class BulldozerDtmProviderProvider(QgsProcessingProvider):
    """ Provider class for Bulldozer DTM Provider """

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        group = self.name()
        ProcessingConfig.settingIcons[group] = self.icon()
        ProcessingConfig.addSetting(Setting(group, BulldozerDtmProviderSettings.ACTIVATE,
                                            self.tr('Activate'), True))

        self.addAlgorithm(BulldozerDtmProviderAdvancedAlgorithm())
        self.addAlgorithm(BulldozerDtmProviderConfigFileAlgorithm())
        self.addAlgorithm(BulldozerDtmProviderGenerateConfigFile())

    def validateBulldozerInstall(self, folder):
        """
        Check that Bulldozer has been installed in the given venv
        Else, tries tot install it

        :return:
        """

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'Bulldozer'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Bulldozer')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """

        return QIcon(':/plugins/bulldozerdtmprovider/img/bulldozer_logo.png')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
