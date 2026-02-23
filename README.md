# ColStudies

ColStudies is a lightweight user interface to the  Colectica Repository API. You can see metadata for studies and register DOIs via da|ra. It uses justpy and python.

This project was inspired by the Colectica API from CLOSER, available at 
<https://github.com/CLOSER-Cohorts/colectica-api>

## Changes

### Version 0.91
Coreected:
- Removed duplicate "ZA" in cdc exports
- Updated python modules and requirements

### Version 0.9
Added:
- Python script cdcstudies.py can export CESSDA CDC format of the studies that have a GESIS Study Number 
- Requirements are to enter in settings.py: colecticahostname, colecticausername, colecticapassword
- This script can be run without the JustPy server being started: `python web/cdcstudies.py`

### Version 0.8
Added:
- STAR info shows files present in DBKEdit but not in STAR folder; they can now be deleted by selection

### Version 0.7
Improved:
- da|ra login page added for easier use.
- da|ra accepts direct registration, not only a draft
- DBKEdit STAR files properties now support option to export SPSS and export language

### Version 0.6
Several improvements have been added:
- Added a menu item for Search: This allows to search Colectica studies and display the list of results.
- Search function has an option to display the Study Number of the study.
- DBKEdit login page added for easier use.
- Star info is now displayed in different colors to see which source it has.
- Star info can now be edited to include correct document type and remark fields in English and German.


### Version 0.5
Sign in to DBKEdit if no Username/Password specified in settings. Prepare file and annotations functions.


### Version 0.4
Added functions to manage local Files (STAR folders) and send them to DBKEdit database (GESIS specific functions).


## Usage

1) Configuration of user settings can be done in `settings.py`

2) Configuration of server settings can be done in `justpy.env`

3) To start the server, double-click on `StartColStudies.cmd`
   - basic information about status and errors are shown in the console
   - you can also use python to start the main file colstudies.py
   - `python web/colstudies.py`

4) This will open your default browser with the start page
   - click 'reload' to refresh if it does not so automatically

5) To use ColStudies, login with your Colectica Repository account 


## Dependencies

ColStudies uses JustPy and Python 3

Install Python dependencies with `python -m pip install -r requirements.txt`

Pin and upgrade dependencies with

```
python -m pip install pip-tools
python -m piptools compile --upgrade --extra dev --allow-unsafe --generate-hashes pyproject.toml
```

## License

License: MIT License

Copyright (c) 2026 Wolfgang Zenk-Möltgen, GESIS


[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
