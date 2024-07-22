<div align="center">
    <img src="https://raw.githubusercontent.com/CNES/bulldozer/master/docs/source/images/bulldozer_logo.png" width=256>


**Bulldozer, a DTM extraction tool requiring only a DSM as input.**

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI Version](https://img.shields.io/pypi/v/bulldozer-dtm?color=%2334D058&label=pypi%20package)](https://pypi.org/project/bulldozer-dtm/)
[![Documentation](https://readthedocs.org/projects/bulldozer/badge/?version=stable)](https://bulldozer.readthedocs.io/?badge=stable)
</div>

---

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#installation">Installation</a> •
  <a href="#quickstart">Quick Start</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#contribute">Contribute</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#licence">Licence</a> •
  <a href="#credits">Credits</a>
</p>

</div>

---
## Overview

<div align="center">
<img src="https://raw.githubusercontent.com/CNES/bulldozer/master/docs/source/images/result_overview.gif" alt="demo" width="400"/>
</div>


The Bulldozer QGIS Processing provider is designed to enhance digital terrain modeling within QGIS.
It integrates seamlessly with QGIS's Processing framework, offering three main algorithms to cater to different user needs:

1. **Basic Algorithm**: Provides a simple setup with an input DTM and an output folder.
2. **Config File Algorithm**: Uses an input configuration file to dynamically set parameters.
3. **Advanced Algorithm**: Gives users access to all customizable parameters of the Bulldozer.


## Quickstart

### Installation

#### Prerequisites
- QGIS version 3.0 or higher
- internet access

#### Installation Steps
You can install the plugin directly from within QGIS:
  1. Go to `Plugins > Manage and Install Plugins`.
  2. Search for "BulldozerDtmProvider".
  3. Click `Install Plugin`.


#### Alternative Installation
You can also install the plugin manually:
1. **Download**: Download the latest version of the plugin from the [QGIS Plugin Hub](https://plugins.qgis.org/) or [Gitlab repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin).
2. **Install**: Copy the plugin files into your QGIS plugin directory, typically located at:
   - Windows: `C:\Users\[username]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. **Restart QGIS**: Restart QGIS to load the new plugin.



### Running Algorithms

All the algorithms can be accessed through the QGIS Processing Toolbox under `3D/Rater`. Search for "Bulldozer" to find the algorithms.

1. **Basic Algorithm**:
   - Inputs: DTM file path, output folder path.

2. **Config File Algorithm**:
   - Inputs: Path to configuration file.

3. **Advanced Algorithm**:
   - Inputs: Detailed parameters as specified in the advanced settings.


## Documentation

* Bulldozer can be found [here](https://github.com/CNES/bulldozer)
* Go to **Bulldozer** [main documentation](https://bulldozer.readthedocs.io/?badge=latest) for more information
* [Developper guide](docs/README.md)


## Contribute

To do a bug report or a contribution, see the [**Contribution Guide**](CONTRIBUTING.md).
for any help or suggestion, feel free to contact the authors:

### !!! TBD FIXME


## Troubleshooting
For common issues and their solutions, visit the [Issues section of our Gitlab repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin/-/issues).

## License
The **Bulldozer plugin** is released under GPL V2. For details, see the **Bulldozer** [LICENSE](LICENSE) file in the repository.

## Credits

Please refer to the [Authors file](AUTHORS.md).

## Reference

 [D. Lallement, P. Lassalle, Y. Ott, R. Demortier, and J. Delvit, 2022. BULLDOZER: AN AUTOMATIC SELF-DRIVEN LARGE SCALE DTM EXTRACTION METHOD FROM DIGITAL SURFACE MODEL. ISPRS - International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences.](https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLIII-B2-2022/409/2022/)
