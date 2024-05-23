# Bulldozer QGIS Processing Provider

## Overview
The Bulldozer QGIS Processing provider is designed to enhance digital terrain modeling within QGIS.
It integrates seamlessly with QGIS's Processing framework, offering three main algorithms to cater to different user needs:

1. **Basic Algorithm**: Provides a simple setup with an input DTM and an output folder.
2. **Config File Algorithm**: Uses an input configuration file to dynamically set parameters.
3. **Advanced Algorithm**: Gives users access to all customizable parameters of the Bulldozer.

## Installation

### Prerequisites
- QGIS version 3.0 or higher
- internet access

### Installation Steps
You can install the plugin directly from within QGIS:
  1. Go to `Plugins > Manage and Install Plugins`.
  2. Search for "BulldozerDtmProvider".
  3. Click `Install Plugin`.


### Alternative Installation
You can also install the plugin manually:
1. **Download**: Download the latest version of the plugin from the [QGIS Plugin Hub](https://plugins.qgis.org/) or [Gitlab repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin).
2. **Install**: Copy the plugin files into your QGIS plugin directory, typically located at:
   - Windows: `C:\Users\[username]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. **Restart QGIS**: Restart QGIS to load the new plugin.



## Usage

### Running Algorithms

All the algorithms can be accessed through the QGIS Processing Toolbox under `3D/Rater`. Search for "Bulldozer" to find the algorithms.

1. **Basic Algorithm**:
   - Inputs: DTM file path, output folder path.

2. **Config File Algorithm**:
   - Inputs: Path to configuration file.

3. **Advanced Algorithm**:
   - Inputs: Detailed parameters as specified in the advanced settings.


## Troubleshooting
For common issues and their solutions, visit the [Issues section of our Gitlab repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin/-/issues).

## License
The Bulldozer plugin is released under GPL V2. For details, see the LICENSE file in the repository.
