# pip install requests
# pip install configparser

import requests
from requests.auth import HTTPBasicAuth
import configparser
import json
import glob
import argparse
import re
import zipfile
import os
from os.path import exists
import shutil
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# defaults
parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--debug", "-d", help="For debugging", action=argparse.BooleanOptionalAction)
parser.add_argument("--config", help="Config Filename", default="config.ini")
parser.add_argument("--remove-dups", help="Remove Duplicate Content Pack Verions.", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--import", help="Import json files.", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--import-dir", help="Directory to import json content pack files from. Path is relative to script working directory.", default="spotlights")
parser.add_argument("--verbose", help="Verbose output.", action=argparse.BooleanOptionalAction, default=False)

args = parser.parse_args()
configFromArg = vars(args)


# font
#           Style
#           v Color
#           v v  Background
#           v v  v
defText = "\033[0;30;50m"
alertText = "\033[1;33;50m"
errorText = "\033[1;31;50m"
successText = "\033[1;32;50m"

print(defText)

# Colors
# 
# Example
# Text Style;Color;Background
# 
# Text Style
#   No Effect   0
#   Bold        1
#   Underline   2
#   Negative1   3
#   Negative2   5
# 
# Color
#   Black       30
#   Red         31
#   Green       32
#   Yellow      33
#   Blue        34
#   Purple      35
#   Cyan        36
#   White       37
# 
# Backgrounds
#   Black       40
#   Red         41
#   Green       42
#   Yellow      43
#   Blue        44
#   Purple      45
#   Cyan        46
#   White       47

print("Arguments: ")
print(configFromArg)
print("")

sAuthFile = configFromArg['config']
sImportDir = configFromArg['import_dir']

if configFromArg['debug']:
    print("DEBUG ENABLED")
    print("")

# load config file for server info, auth info
config = configparser.ConfigParser()
config.read(sAuthFile)

# build URI
sArgBuildUri = ""
sArgHttps = config['DEFAULT']['https']
if sArgHttps == "true":
    sArgBuildUri = "https://"
else:
    sArgBuildUri = "http://"

sArgHost = config['DEFAULT']['host']
sArgPort = config['DEFAULT']['port']
sArgUser = config['DEFAULT']['user']
sArgPw = config['DEFAULT']['password']

# print("Graylog Server: " + sArgHost)
print(alertText + "Graylog Server: " + sArgHost + defText + "\n")

# build server:host and concat with URI
sArgBuildUri=sArgBuildUri+sArgHost+":"+sArgPort

def uploadContentPack(oJsonFile):
    # specify URL
    sUrl = sArgBuildUri + "/api/system/content_packs"

    # headers
    sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}

    # send req, upload json content pack file
    r = requests.post(sUrl, json = oJsonFile, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
    return r

def installContentPack(sContentPackUniqueId, sContentPackRevVer):
    # specify URL
    sUrl = sArgBuildUri + "/api/system/content_packs/" + sContentPackUniqueId + "/" + str(sContentPackRevVer) + "/installations"
    
    # headers
    sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}

    # {"parameters":{},"comment":""}


    # send req, upload json content pack file
    oJson = {"parameters":{},"comment":""}
    r = requests.post(sUrl, json = oJson, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))

    # print(r.status_code)
    # print(r.headers)
    # print(r.text)
    return r



def fullUploadInstallContentPack(sArgUploadFile):
    # load json file
    f = open (sArgUploadFile, "r")
    oJsonFile = json.loads(f.read())
    # get ID
    sContentPackUniqueId = oJsonFile['id']
    sContentPackRevVer = oJsonFile['rev']

    print("Installing Content Pack:")
    print("    " + oJsonFile['name'])
    # print("    " + sContentPackUniqueId)

    if configFromArg['debug']:
        print("        debug enabled, skipping upload web req")

    if not configFromArg['debug']:
        r = uploadContentPack(oJsonFile)

        iStatusCode = r.status_code
        if iStatusCode == 201:
            print("    Content Pack Successfully Uploaded")
            print("    Will Install...")
            rInst = installContentPack(sContentPackUniqueId, sContentPackRevVer)
            if rInst.status_code == 200:
                print("        " + successText + "Installed Successfully!" + defText)
            else:
                print("        " + errorText + "Error: " + str(rInst.status_code) + " (" + rInst.text + ")" + defText)
        elif iStatusCode == 401:
            print("")
            print(errorText + "ERROR! Authentication error. Please verify config file is configured correctly." + defText)
            print("")
            exit()
        elif iStatusCode == 400:
            print("        " + successText + "Already Installed!" + defText)
            if configFromArg['verbose']:
                print("    " + errorText + "Error: " + str(iStatusCode) + " (" + r.text + ")" + defText)
        else:
            print("    " + errorText + "Error: " + str(iStatusCode) + " (" + r.text + ")" + defText)
    
    print("")

    # print(r.status_code)
    # print(r.headers)
    # print(r.text)

def getLatestIlluminateContentPacks():
    # lIllCtPkIds = []
    dictIlluminateContentPacks = {}

    print("Getting list of content packs...")

    # specify URL
    sUrl = sArgBuildUri + "/api/system/content_packs/latest"

    # headers
    sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}

    if configFromArg['verbose']:
        print("requests.get: " + sUrl)
    r = requests.get(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
    if r.status_code == 200:
        intIllCtPk = 0

        # print(r.text)
        oJsonContentPacks = json.loads(r.text)
        # print("        Found " + str(oJsonContentPacks['total']) + " content packs.")

        regex = r"Graylog Illuminate"

        for ctpk in oJsonContentPacks['content_packs']:
            if re.match(regex, ctpk['name']):
                intIllCtPk += 1

        print("    Found " + str(intIllCtPk) + " Illuminate content packs.")

        for ctpk in oJsonContentPacks['content_packs']:
            if re.match(regex, ctpk['name']):
                if configFromArg['verbose']:
                    print("        Illumate Content Pack: " + ctpk['name'])
                    print("            ID: " + ctpk['id'] + ", Rev: " + str(ctpk['rev']))
                # lMetaKeys.append(ctpk['id'])
                dictIlluminateContentPacks[ctpk['id']] = {'rev': ctpk['rev'], 'name': ctpk['name']}

        return dictIlluminateContentPacks


    else:
        print("    " + errorText + "ERROR! HTTP Status: " + str(r.status_code) + defText)

def doUninstallContentPackRevById(argContentPackId, argContentPackRevId):
    print("        Uninstalling Content Pack: " + argContentPackId + ", rev: " + argContentPackRevId)

    # specify URL
    sUrl = sArgBuildUri + "/api/system/content_packs/" + argContentPackId + "/installations/" + argContentPackRevId

    # headers
    sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}

    r = requests.delete(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
    print("        HTTP Status:" + str(r.status_code))

def doCompareFindIfOldRevsCanBeUninstalled(argJsonContentPackAllRevs):
    listRevs = []
    listUniques = []
    dictIlluminateContentPackInstallRevs = {}

    # get revs
    for ctPkRev in argJsonContentPackAllRevs:
        realRev = ctPkRev['content_pack_revision']
        listRevs.append(realRev)
        dictIlluminateContentPackInstallRevs[realRev] = ctPkRev
    
    listRevs.sort(reverse=True)

    isRevUnique = True
    
    for revNumber in listRevs:
        # entities
        jsEnt = dictIlluminateContentPackInstallRevs[revNumber]['entities']
        for entity in jsEnt:
            strType = entity['type']['name']
            strTitle = entity['title']
            # print("Type: " + strType + ", Title: " + strTitle)
            strConcatUnique = strType + "___" + strTitle

            # is this unique?
            if strConcatUnique in listUniques:
                # print("            NOT UNIQUE: " + strConcatUnique)
                isRevUnique = False
                break

            listUniques.append(strConcatUnique)
        
        if not isRevUnique:
            print("    " + alertText + "Version: " + str(revNumber) + " is not unique" + defText)
            strContentPackId = dictIlluminateContentPackInstallRevs[revNumber]['content_pack_id']
            strInstallId = dictIlluminateContentPackInstallRevs[revNumber]['_id']
            # print("strContentPackId: " + strContentPackId)
            # print("strInstallId: " + strInstallId)
            if not configFromArg['debug']:
                doUninstallContentPackRevById(strContentPackId, strInstallId)
            else:
                print("        debug enabled, skipping uninstall content pack version!")
    
    if isRevUnique:
        print("    No duplicate content found.")



def doRemoveDuplicateContentPackVerionInstalls(argContentPackId, argContentPackName):
    iFoundRevs = 0

    # print("")
    # print(argContentPackId)

    # specify URL
    sUrl = sArgBuildUri + "/api/system/content_packs/" + argContentPackId + "/installations"

    # headers
    sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}

    r = requests.get(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
    if r.status_code == 200:
        oJsonContentPack = json.loads(r.text)
        for ctPkRev in oJsonContentPack['installations']:
            iFoundRevs += 1
            # rev = oJsonContentPack['installations'][ctPkRev]['rev']
            rev = ctPkRev['content_pack_revision']
        
        # print("    Found " + str(iFoundRevs) + " revs")
        if iFoundRevs > 1 :
            # more than one, we may have duplicates
            # check if old rev has anything new rev does not
            print("")
            print("Content pack '" + argContentPackName + "' has " + str(iFoundRevs) + " version")
            print("    Checking for duplicate content...")
            doCompareFindIfOldRevsCanBeUninstalled(oJsonContentPack['installations'])

    else:
        print("    ERROR! HTTP Status: " + str(r.status_code))

def doCheckForDuplicateContentPacks():
    dictContentPacksLatest = getLatestIlluminateContentPacks()
    for key in dictContentPacksLatest:
        jsonContentPack = doRemoveDuplicateContentPackVerionInstalls(key, dictContentPacksLatest[key]['name'])

def listdirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

def doUnzipFile(path_to_zip_file):
    sFileExt = path_to_zip_file[-4:]

    # verify file ext is .zip
    if not sFileExt.lower() == ".zip":
        print(errorText + "ERROR: file extension is not .zip" + defText)
        return None

    # verify the specified file exists
    if not exists(path_to_zip_file):
        print(errorText + "ERROR: file " + path_to_zip_file + " does not exist!" + defText)
        return None
    
    
    # iLen = len(path_to_zip_file)
    # iNewLen = iLen - 4
    sExtractFolder = "extract"
    if exists(sExtractFolder):
        print(alertText + "Warning: Folder " + sExtractFolder + " already exists. Deleting." + defText)
        # shutil.rmtree(sExtractFolder)
    
    # with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    #     zip_ref.extractall(sExtractFolder)

    if exists(sExtractFolder):
        # extract successful
        # get child items
        # dir_list =  os.listdir(sExtractFolder)
        dir_list = listdirs(sExtractFolder)
        
        if len(dir_list) > 0:
            return sExtractFolder + "/" + dir_list[0]
    else:
        print(errorText + "ERROR! Extraction failed!")

def getBundleZipFileName(arg_folder):
    # print(arg_folder)
    dir_list =  os.listdir(arg_folder)
    for file in dir_list:
        # print(file)
        file_ext = file[-4:]
        if file_ext.lower() == ".zip":
            return arg_folder + "/" + file











# extracted_folder = doUnzipFile("graylog_illuminate_standard.v3.1.0.zip")
# dir_spotlights = extracted_folder + "/" + "spotlights"
# ill_bundle_zip = getBundleZipFileName(extracted_folder)

# exit()


# getContentPack("78f8f6ed-ce4c-4033-8be8-23bb6e92f058")
# exit()







if configFromArg['import']:
    print("================================================================================")
    print("Installing Content Packs from " + sImportDir)
    print("")

    oFiles = glob.glob("spotlights/*.json")
    for file in oFiles:
        fullUploadInstallContentPack(file)

if configFromArg['remove_dups']:
    print("================================================================================")
    print("Checking for duplicate Illuminate content packs...")
    print("")

    # disable duplicates
    doCheckForDuplicateContentPacks()

exit()