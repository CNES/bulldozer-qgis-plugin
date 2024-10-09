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

import os.path
import sys
import pip
from pathlib import Path


try:
    from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
except ImportError:
    print("Bulldozer not found in current python path, trying to find it...")
    venv_folder = os.path.join(os.path.dirname(__file__), "bulldozer-dtm_venv")
    os.environ["PATH"] += f":{os.path.join(venv_folder, 'local', 'bin')}"
    sys.path.append(venv_folder)

    try:
        from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
    except (ImportError, ModuleNotFoundError):

        print("Bulldozer not found in bulldozer-dtm subdir, trying to install it...")
        os.makedirs(venv_folder, exist_ok=True)
        pip.main(["install", "--target", venv_folder, "bulldozer-dtm"])
        sys.path.insert(0, venv_folder)

        try:
            from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
        except (ImportError, ModuleNotFoundError):

            print("Can't import bulldozer from new installation in bulldozer-dtm, "
                  "trying force it...")
            import importlib.util

            spec = importlib.util.spec_from_file_location("bulldozer",
                                                          os.path.join(venv_folder,
                                                                       "bulldozer/__init__.py"))
            foo = importlib.util.module_from_spec(spec)
            sys.modules["bulldozer"] = foo
            spec.loader.exec_module(foo)
            import bulldozer
            from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
            print("Import Bulldozer-dtm OK")
