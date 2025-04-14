<div align="center">
    <img src="https://raw.githubusercontent.com/CNES/bulldozer/master/docs/source/images/logo.png" width=256>


**Bulldozer, a DTM extraction tool requiring only a DSM as input.**

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI Version](https://img.shields.io/pypi/v/bulldozer-dtm?color=%2334D058&label=pypi%20package)](https://pypi.org/project/bulldozer-dtm/)
[![Documentation](https://readthedocs.org/projects/bulldozer/badge/?version=stable)](https://bulldozer.readthedocs.io/?badge=stable)
</div>

---
## Overview

<div align="center">
<img src="https://raw.githubusercontent.com/CNES/bulldozer/master/docs/source/images/result_overview.gif" alt="demo" width="400"/>
</div>


The Bulldozer QGIS Processing provider is designed to extract Digital Terrain Model (DTM) from raster format Digital Surface Model (DSM) using[Bulldozer](https://github.com/CNES/bulldozer).
It integrates seamlessly with QGIS's Processing framework, offering three main algorithms to cater to different user needs:

1. **Basic Algorithm**: Provides a simple setup with an input DTM and an output folder.
2. **Config File Algorithm**: Uses an input configuration file to dynamically set parameters.
3. **Advanced Algorithm**: Gives users access to all customizable parameters of the Bulldozer.


## Quickstart

### Installation

#### Prerequisites
- QGIS version 3.0 or higher

#### Installation Steps
You can install the plugin directly from within QGIS:
  1. Go to `Plugins > Manage and Install Plugins`.
  2. Search for "BulldozerDtmProvider".
  3. Click `Install Plugin`.


#### Alternative Installation
You can also install the plugin manually:
1. **Download**: Download the latest version of the plugin from the [QGIS Plugin Hub](https://plugins.qgis.org/) or [Github repository](https://github.com/CNES/bulldozer-qgis-plugin).
2. **Install**: Copy the plugin files into your QGIS plugin directory, typically located at:
   - Windows: `C:\Users\[username]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. **Restart QGIS**: Restart QGIS to load the new plugin.



### Running Algorithms

<!---TODO : update this part-->
All the algorithms can be accessed through the QGIS Processing Toolbox under `3D/Rater`. Search for "Bulldozer" to find the algorithms.

1. **Basic Algorithm**:
   - Inputs: DTM file path, output folder path.

2. **Config File Algorithm**:
   - Inputs: Path to configuration file.

3. **Advanced Algorithm**:
   - Inputs: Detailed parameters as specified in the advanced settings.


## Documentation

* **Bulldozer** [main documentation](https://bulldozer.readthedocs.io/?badge=latest)
* [Developper guide](docs/README.md)
## License

The **Bulldozer QGIS plugin** is released under GPL V2. For details, see the [LICENSE](LICENSE) file in the repository.
**Bulldozer** is licensed under Apache License v2.0. Please refer to the [LICENSE](https://github.com/CNES/bulldozer/blob/master/LICENSE) file for more details.

## <a name="Citation"></a>Citation
If you use **Bulldozer** in your research, please cite the following paper:
```text
@article{bulldozer2023,
  title={Bulldozer, a free open source scalable software for DTM extraction},
  author={Dimitri, Lallement and Pierre, Lassalle and Yannick, Ott},
  journal = {The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences},
  volume = {XLVIII-4/W7-2023},
  year = {2023},
  pages = {89--94},
  url = {https://isprs-archives.copernicus.org/articles/XLVIII-4-W7-2023/89/2023/},
  doi = {10.5194/isprs-archives-XLVIII-4-W7-2023-89-2023}
}
```