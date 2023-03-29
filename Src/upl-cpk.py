# pip install requests
# pip install configparser

import time
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
parser.add_argument("--illuminate-zip", help="Parent Zip file for illuminate release. NOTE: this is NOT the bundle zip!", default="")
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
    bApiHttps = True
else:
    sArgBuildUri = "http://"
    bApiHttps = False

sArgHost = config['DEFAULT']['host']
sArgPort = config['DEFAULT']['port']
sArgUser = config['DEFAULT']['user']
sArgPw = config['DEFAULT']['password']

dictGraylogApi = {
    "https": bApiHttps,
    "host": sArgHost,
    "port": sArgPort,
    "user": sArgUser,
    "password": sArgPw
}

# ================= BACKOFF START ==============================

# Number of seconds to wait before retrying after a socket error
iSocketRetryWaitSec = 5

# Maximum number of retries to attempt. script exits if max is reach so be careful!
iSocketMaxRetries = 300

# How many seconds to add before each retry
# backoff resets after a successful connection
iSocketRetryBackOffSec = 10

# maximum allowed retry wait in seconds
iSocketRetryBackOffMaxSec = 300

# how many retries before the backoff time is added before each retry
iSocketRetryBackOffGraceCount = 24

# ================= BACKOFF END ================================


bCleanupExtractedDir = False

# print("Graylog Server: " + sArgHost)
print(alertText + "Graylog Server: " + sArgHost + defText + "\n")

# build server:host and concat with URI
sArgBuildUri=sArgBuildUri+sArgHost+":"+sArgPort

def graylogApiConfigIsValid():
    if 'https' in dictGraylogApi:
        if not dictGraylogApi['https'] == True and not dictGraylogApi['https'] == False:
            return False
    else:
        return False
    
    if 'host' in dictGraylogApi:
        if not len(dictGraylogApi['host']) > 0:
            return False
    else:
        return False

    if 'port' in dictGraylogApi:
        if not len(dictGraylogApi['port']) > 0 and not int(dictGraylogApi['port']) > 0:
            return False
    else:
        return False

    if 'user' in dictGraylogApi:
        if not len(dictGraylogApi['user']) > 0:
            return False
    else:
        return False

    if 'password' in dictGraylogApi:
        if not len(dictGraylogApi['password']) > 0:
            return False
    else:
        return False
    
    return True

def mergeDict(dictOrig: dict, dictToAdd: dict, allowReplacements: bool):
    for item in dictToAdd:
        
        bSet = True
        if item in dictOrig:
            if allowReplacements == False:
                bSet = False
        
        if bSet == True:
            dictOrig[item] = dictToAdd[item]
    
    return dictOrig

def doGraylogApi(argMethod: str, argApiUrl: str, argHeaders: dict, argJson: dict, argFiles: dict, argExpectedReturnCode: int, argReturnJson: bool):
    if graylogApiConfigIsValid() == True:
        # build URI
        sArgBuildUri = ""
        if dictGraylogApi['https'] == True:
            sArgBuildUri = "https://"
        else:
            sArgBuildUri = "http://"

        sArgHost    = dictGraylogApi['host']
        sArgPort    = dictGraylogApi['port']
        sArgUser    = dictGraylogApi['user']
        sArgPw      = dictGraylogApi['password']

        # print(alertText + "Graylog Server: " + sArgHost + defText + "\n")

        # build server:host and concat with URI
        sArgBuildUri=sArgBuildUri+sArgHost+":"+sArgPort
        
        sUrl = sArgBuildUri + argApiUrl

        # add headers
        sHeaders = {"Accept":"application/json", "X-Requested-By":"python-ctpk-upl"}
        sHeaders = mergeDict(sHeaders, argHeaders, True)
        
        if argMethod.upper() == "GET":
            try:
                r = requests.get(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
            except Exception as e:
                return {
                    "success": False,
                    "exception": e
                }
        elif argMethod.upper() == "POST":
            if argFiles == False:
                try:
                    r = requests.post(sUrl, json = argJson, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
                except Exception as e:
                    return {
                        "success": False,
                        "exception": e
                    }
            else:
                try:
                    r = requests.post(sUrl, json = argJson, files=argFiles, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
                except Exception as e:
                    return {
                        "success": False,
                        "exception": e
                    }
        
        if r.status_code == argExpectedReturnCode:
            if argReturnJson:
                return {
                    "json": json.loads(r.text),
                    "status_code": r.status_code,
                    "success": True
                }
            else:
                return {
                    "text": r.text,
                    "status_code": r.status_code,
                    "success": True
                }
        else:
            return {
                "status_code": r.status_code,
                "success": False,
                "failure_reason": "Return code " + str(r.status_code) + " does not equal expected code of " + str(argExpectedReturnCode),
                "text": r.text
            } 
    else:
        return {"msg": "api_not_configured"}

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

            bIsIlluminateContentPack = False
            
            if re.match(regex, ctpk['name']):
                bIsIlluminateContentPack = True

            if re.match(r"Graylog", ctpk['vendor']) and ctpk['name'].lower() == "default summary templates":
                # print(alertText + "MATCH Default Summary Templates" + defText)
                bIsIlluminateContentPack = True

            if bIsIlluminateContentPack == True:
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
        shutil.rmtree(sExtractFolder)
    
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(sExtractFolder)

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

def uploadIlluminateBundleZip(argIllBundleFile):
    bActivateBundle = False
    dHeaders = {
        "Accept": "*/*",
        "X-Requested-By":"python-ctpk-upl"
    }

    files = {'file': open(argIllBundleFile,'rb')}

    r = doGraylogApi("POST", "/api/plugins/org.graylog.plugins.illuminate/bundles/upload", dHeaders, {}, files, 200, False)
    print(r)
    
    if 'success' in r:
        if r['success'] == True:
            # get uploaded bundle name so we can activate it
            if 'text' in r:
                illBundleVerName = r['text']
                bActivateBundle = True
        else:
            if 'text' in r:
                if re.search("already exists", str(r['text']), re.IGNORECASE) and int(r['status_code']) == 403:
                    illBundleVerName = re.search(r"Bundle version '(v\d+\.\d+\.\d+)' ", r['text'], re.IGNORECASE).group(1)
                    bActivateBundle = True
                    print(alertText + "Illuminate Bundle " + successText + illBundleVerName + alertText + " already exists. Will activate." + defText)
    
    if bActivateBundle == True:
        dJsonActivateIllBundle = {
            "enabled":True
        }
        r = doGraylogApi("POST", "/api/plugins/org.graylog.plugins.illuminate/bundles/" + illBundleVerName, dHeaders, dJsonActivateIllBundle, False, 204, False)
        if 'success' in r:
            if r['success'] == True:
                return True
    
    return False

def do_wait_until_online():
    iSocketRetries = 0
    iSocketInitialRetryBackOff = iSocketRetryWaitSec

    while iSocketRetries < iSocketMaxRetries:
        if iSocketRetries > 0:
            print("Retry " + str(iSocketRetries) + " of " + str(iSocketMaxRetries))

        r = doGraylogApi("GET", "/api/", {}, {}, False, 200, True)
        if 'success' in r:
            if r['success'] == False:
                if "exception" in r:
                    print(errorText)
                    print(r["exception"])
                    print(defText)

                    print("Waiting " + str(iSocketInitialRetryBackOff) + "s Max backoff: " + str(iSocketRetryBackOffMaxSec) + "s)...")
                    # sleep for X seconds
                    time.sleep(iSocketInitialRetryBackOff)

                    # Increment socket retry count
                    iSocketRetries = iSocketRetries + 1

                    # If the number of retries exceeds the intial backoff retry grace count
                    #   Don't apply backoff for the first X number of retries in case the error was short lived
                    if iSocketRetries > iSocketRetryBackOffGraceCount:
                        # if backoff value is less than max, keep adding backoff value to delay
                        if iSocketInitialRetryBackOff < iSocketRetryBackOffMaxSec:
                            iSocketInitialRetryBackOff = iSocketInitialRetryBackOff + iSocketRetryBackOffSec

                        # if backoff value exceeds max, set to max
                        if iSocketInitialRetryBackOff > iSocketRetryBackOffMaxSec:
                            iSocketInitialRetryBackOff = iSocketRetryBackOffMaxSec

                    # If socket retries exceeds max, exit script
                    if iSocketRetries > iSocketMaxRetries:
                        print("ERROR! To many socket retries")
                        return False

            elif r['success'] == True:
                print(successText + "Graylog Cluster is Online" + defText)
                return True
    return False

do_wait_until_online()

if len(configFromArg['illuminate_zip']):
    illuminate_release_zip = configFromArg['illuminate_zip']
    # 1. Extract parent zip
    extracted_folder = doUnzipFile(illuminate_release_zip)
    bCleanupExtractedDir = True

    dir_spotlights = extracted_folder + "/" + "spotlights"
    sImportDir = dir_spotlights

    # 2. get name/path of illuminate bundle zip
    ill_bundle_zip = getBundleZipFileName(extracted_folder)

    # 3. Upload Zip
    bUplSuccess = uploadIlluminateBundleZip(ill_bundle_zip)
    if bUplSuccess == True:
        print(successText + "Illuminate Bundle " + defText + ill_bundle_zip + successText + " successfully uploaded and activated." + defText)
    else:
        print(errorText + "ERROR! Illuminate bundle failed to upload and activate." + defText)

if configFromArg['import']:
    print("================================================================================")
    print("Installing Content Packs from " + sImportDir)
    print("")

    oFiles = glob.glob(sImportDir + "/*.json")
    for file in oFiles:
        fullUploadInstallContentPack(file)

if configFromArg['remove_dups']:
    print("================================================================================")
    print("Checking for duplicate Illuminate content packs...")
    print("")

    # disable duplicates
    doCheckForDuplicateContentPacks()

# cleanup

if bCleanupExtractedDir == True:
    shutil.rmtree("./extract")

exit()