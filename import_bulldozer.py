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

import importlib
import os
import subprocess
import sys
import pip


def setup_bulldozer():
    try:
        from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
        return dsm_to_dtm
    except ImportError:
        print("Bulldozer not found in current python path, trying to find it...")
        venv_folder = os.path.join(os.path.dirname(__file__), "bulldozer-dtm_venv")

        scripts_folder = os.path.join(venv_folder, "Scripts" if os.name == "nt" else "local/bin")

        # Ajouter le dossier venv au PATH et à sys.path
        os.environ["PATH"] += os.pathsep + scripts_folder

        # Ajouter le chemin au sys.path si nécessaire
        if venv_folder not in sys.path:
            sys.path.insert(0, venv_folder)

        try:
            from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
            print("Import Bulldozer-dtm OK")
            return dsm_to_dtm
        except (ImportError, ModuleNotFoundError):

            print("Bulldozer not found in bulldozer-dtm subdir, trying to install it...")
            os.makedirs(venv_folder, exist_ok=True)


            python_executable = os.path.join(sys.prefix, "python.exe") if os.name == "nt" else "python"
            # nt = windows
            if os.name == "nt":

                subprocess.check_call([
                    python_executable,
                    "-m",
                    "pip",
                    "install",
                    "--target",
                    venv_folder,
                    "bulldozer-dtm"
                ])

            else:
                pip.main(["install", "--target", venv_folder, "bulldozer-dtm"])

            # Forcer le rechargement des modules
            importlib.invalidate_caches()
            if "bulldozer" in sys.modules:
                del sys.modules["bulldozer"]
            sys.path.insert(0, venv_folder)

            try:
                from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
                print("Import Bulldozer-dtm OK")
                return dsm_to_dtm
            except (ImportError, ModuleNotFoundError):

                print("Can't import bulldozer from new installation in bulldozer-dtm, "
                    "trying force it...")

                spec = importlib.util.spec_from_file_location("bulldozer",
                                                              os.path.join(venv_folder,
                                                                           "bulldozer",
                                                                           "__init__.py"))
                foo = importlib.util.module_from_spec(spec)
                sys.modules["bulldozer"] = foo

                # Forcer le rechargement des modules
                importlib.invalidate_caches()
                spec.loader.exec_module(foo)
                try:
                    import bulldozer
                    from bulldozer.pipeline.bulldozer_pipeline import dsm_to_dtm
                    print("Import Bulldozer-dtm OK")
                    return dsm_to_dtm
                except ImportError:
                    print("Failed to import Bulldozer even after installation.")
                    raise

# Initialiser Bulldozer
dsm_to_dtm = setup_bulldozer()
