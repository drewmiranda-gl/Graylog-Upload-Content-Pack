# Graylog-Upload-Content-Pack

Automate uploading and install Graylog Content Pack `.json` files.
## What is this?

This is a python script that enumerates all `.json` files in `./spotlights`, and uses the Graylog API to:

1. Upload the contents of the `.json` file (content pack)
2. Install the content pack using the id and rev (version) from the `.json` file
3. Check if old version of same content pack contains any unique content, if it does not, uninstall it so there is no duplicate content (e.g. dashboards)
    * Use `--remove-dups` argument. Disabled by default.

Rudimentary error checking verifies the uploaded json succeeded (HTTP 201) before attempting to call the install API URI.

## How to use?

Requirements/Prereqs:

* Local copy of this repo (e.g. via `git clone`)
* Python 3 (tested on 3.9.13)
* Python modules
    * requests (`pip install requests`)
    * configparser (`pip install configparser`)
* Configure contents of `config.ini`

Instructions:

1. place all `.json` content pack files in sub directory `spotlights`
    * This directory needs to exist at the same level as the `.py` script
    * **ALL** `.json` files will be uploaded and installed
2. execute python script:
    * `python3 upl-cpk.py`

### config.ini

Argument | Description
---- | ----
https | true/false . If true, web URL will use HTTPS.
host | server to connect to for graylog api.
port | port to connect to for graylog api.
user | Graylog user that has access to run API actions.
password | password for user.
### Command Line Arguments

```
optional arguments:
  -h, --help            show this help message and exit
  --debug, --no-debug, -d
                        For debugging (default: None)
  --config CONFIG       Config Filename (default: config.ini)
  --remove-dups, --no-remove-dups
                        Remove Duplicate Content Pack Verions. (default: False)
  --import, --no-import
                        Import json files. (default: True)
  --import-dir IMPORT_DIR
                        Directory to import json content pack files from. Path is relative to script working
                        directory. (default: spotlights)
```

## Sample Output

```
drewmiranda@DMIRANDA-MP Src % python3 upl-cpk.py
Installing Content Pack:
    Graylog Illuminate 2.3.0:Core Spotlight
    7f43e0f9-936e-4858-bbf6-be0b5e31ca38
    Error: 400 ({"type":"ApiError","message":"Content pack 7f43e0f9-936e-4858-bbf6-be0b5e31ca38 with this revision 26 already found!"})

Installing Content Pack:
    Graylog Illuminate:Event Definitions;2021-10-16
    c28d8149-c731-4c38-b8ae-703ffaa6acd9
    Error: 400 ({"type":"ApiError","message":"Content pack c28d8149-c731-4c38-b8ae-703ffaa6acd9 with this revision 4 already found!"})

Installing Content Pack:
    Graylog Illuminate 2.3.0:Windows Security Spotlight
    df0c538a-0252-4e8c-8158-231d7af2f405
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate 2.3.0:Palo Alto 9.1.x Spotlight
    d9929aca-e380-48d0-b3e7-fe4072adecdf
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate 2.3.0:Microsoft Sysmon Spotlight
    c8a9e5a5-2cdf-431d-a407-64e9ccadd507
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate 2.3.0:SonicWall NGFW Spotlight
    3f06c971-85e2-456f-ab1c-bbc0b98510fb
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate 2.3.0:Linux Auditbeat Spotlight
    78f8f6ed-ce4c-4033-8be8-23bb6e92f058
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate 2.3.0:Microsoft Defender Antivirus Spotlight
    64b21d41-ee9c-47dc-adf6-30ccbd734dd7
    Content Pack Successfully Uploaded
    Will Install...
        Install Successfully!

Installing Content Pack:
    Graylog Illuminate:Event Definitions;2022-07-14
    c28d8149-c731-4c38-b8ae-703ffaa6acd9
    Error: 400 ({"type":"ApiError","message":"Content pack c28d8149-c731-4c38-b8ae-703ffaa6acd9 with this revision 6 already found!"})

Installing Content Pack:
    Graylog Illuminate:Event Definitions;2022-04-13
    c28d8149-c731-4c38-b8ae-703ffaa6acd9
    Error: 400 ({"type":"ApiError","message":"Content pack c28d8149-c731-4c38-b8ae-703ffaa6acd9 with this revision 5 already found!"})

```