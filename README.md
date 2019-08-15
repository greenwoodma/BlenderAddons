# Blender Addons: A Random Collection

The repository contains a small number of [Blender](https://www.blender.org) addons I've written and is organized
into folders that mirror the set of Blender [addon categories](https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo#category).

## Installing the Addons
Each addon is a self contained file and so can easily be installed from within Blender
via the addon tab of the user preferences dialog.

Note that there are often multiple versions of each addon that target different versions
of Blender. The version number (without any dots) is added to the end of the filename.
You need to pick the higest numbered version that is less than or equal to the version
of Blender you are using. For example, if you are using Blender v2.78 and there are files
ending with `-260.py` and `280.py` then these are known to work with versions of Blender
2.60 and 2.80, so you would pick the first file as 2.60 is the highest version less than
or equal to 2.78.

## Development Practices
To conform with standard Blender best practices the files should be PEP8-80 compliant.
You can test that they are using [Flake8](http://flake8.pycqa.org)
```
python3 -m flake8 <addon.py>
```
If you don't have `flake7` installed you can get it by running the command
```
python3 -m pip install flake8
```
