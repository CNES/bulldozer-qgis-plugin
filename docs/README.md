# Bulldozer QGIS Plugin Developer Guide

## Introduction

This guide provides detailed documentation for the Bulldozer QGIS Plugin. The Bulldozer QGIS Plugin is designed to extract Digital Terrain Model (DTM) from raster format Digital Surface Model (DSM) using [Bulldozer](https://github.com/CNES/bulldozer). It includes basic, advanced, and config file-driven pipelines to suit user needs and scenarios.

## File Structure

Below is the structure of the essential files within the Bulldozer Plugin:

```
.
├── BulldozerDtmProvider_Advanced_algorithm.py
├── BulldozerDtmProvider_algorithm.py
├── BulldozerDtmProvider_Basic_Algorithm.py
├── BulldozerDtmProvider_ConfigFile_algorithm.py
├── BulldozerDtmProvider_provider.py
├── BulldozerDtmProvider.py
├── BulldozerDtmProviderSettings.py
└── import_bulldozer.py
```

### Descriptions

- **BulldozerDtmProvider_algorithm.py**: Base class for all algorithms. Defines common functionalities and structures.
- **BulldozerDtmProvider_Basic_Algorithm.py**: Implements the basic usage scenario with input Digital Surface Model (DSM) and output target folder.
- **BulldozerDtmProvider_Advanced_algorithm.py**: Provides access to all customizable parameters of Bulldozer. It's designed for advanced users.
- **BulldozerDtmProvider_ConfigFile_algorithm.py**: Uses an input configuration file to set Bulldozer parameters.
- **import_bulldozer.py**: Checks for the presence of the `bulldozer-dtm` library in the current environment, installs it if required, and setup the environment accordingly.


## Parameters

Parameters are defined within each algorithm's `initAlgorithm` method. Refer to the individual algorithm files for detailed parameter listings and default values.

## Adding a new file to the project
When adding a new file to this project, please update `Makefile` and `pb_tool.cfg` files.

Look for the section `PY_FILES` in the `Makefile` where source files are listed. Add your new file to the section. For example, you might have a section like this:

```
PY_FILES = \
	__init__.py \
	BulldozerDtmProvider.py\
	BulldozerDtmProvider_Advanced_algorithm.py \
    new_file.py
```

Add the path to the new file in `pb_tool.cfg` in the [files] section.

```
[files]
# Python  files that should be deployed with the plugin
python_files: __init__.py BulldozerDtmProvider.py new_file.py
```


## Resources

- [QGIS Processing Documentation](https://docs.qgis.org/3.34/en/docs/user_manual/processing/scripts.html)
- [Bulldozer GitHub Repository](https://github.com/CNES/bulldozer-qgis-plugin)