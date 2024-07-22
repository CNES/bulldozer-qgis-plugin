# Bulldozer Developer Guide

## Introduction

This guide provides detailed documentation for the Bulldozer QGIS Processing provider. The Bulldozer plugin is designed to enhance digital terrain modeling within QGIS. It includes basic, advanced, and config file-driven functionalities to suit different user needs and scenarios.

## File Structure

Below is the structure of the essential files within the Bulldozer plugin:

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
- **BulldozerDtmProvider_Basic_Algorithm.py**: Implements the basic usage scenario with input digital terrain model (DTM) and output folder specification.
- **BulldozerDtmProvider_Advanced_algorithm.py**: Provides access to all customizable parameters of the Bulldozer, suitable for advanced users.
- **BulldozerDtmProvider_ConfigFile_algorithm.py**: Utilizes an input configuration file to set parameters dynamically.
- **import_bulldozer.py**: Checks for the presence of the `bulldozer-dtm` library in the current environment, installs it if absent, and configures the environment accordingly.


## Parameters

Parameters are defined within each algorithm's `initAlgorithm` method. Refer to the individual algorithm files for detailed parameter listings and default values.

## Adding a new file to the project
When adding a new file to this project, `Makefile` and `pb_tool.cfg` files have to be updated.

Look for the section `PY_FILES` in the `Makefile` where source files are listed. Add your new file to these sections. For example, you might have a section like this:

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
- [Bulldozer GitHub Repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin)

## Contributing

Contributions to the Bulldozer plugin are welcome. To contribute:
- Fork the repository.
- Make your changes and write clear, concise commit messages.
- Submit a pull request detailing the changes made and their purpose.

## Troubleshooting

For common issues and their solutions, visit the [Issues section of our Gitlab repository](https://gitlab.cnes.fr/3d/tools/bulldozer-qgis-plugin/-/issues).
