# pip install requests
# pip install configparser

import requests
from requests.auth import HTTPBasicAuth
import configparser
import json
import glob

# load config file for server info, auth info
config = configparser.ConfigParser()
config.read('auth.ini')

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
    print("    " + sContentPackUniqueId)

    r = uploadContentPack(oJsonFile)

    iStatusCode = r.status_code
    if iStatusCode == 201:
        print("    Content Pack Successfully Uploaded")
        print("    Will Install...")
        rInst = installContentPack(sContentPackUniqueId, sContentPackRevVer)
        if rInst.status_code == 200:
            print("        Install Successfully!")
        else:
            print("        Error: " + str(rInst.status_code) + " (" + rInst.text + ")")
    else:
        print("    Error: " + str(iStatusCode) + " (" + r.text + ")")
    
    print("")

    # print(r.status_code)
    # print(r.headers)
    # print(r.text)

oFiles = glob.glob("spotlights/*.json")
for file in oFiles:
    fullUploadInstallContentPack(file)

exit()









































# misc notes
# ploads = {'things':2,'total':25}
# sUrl = "http://192.168.0.98:9000/api/messages/gl_linux_metricbeat_25/53da9da5-09ff-11ed-bd3c-000c291279c7"
# params=ploads
# headers={"Content-Type":"text"}
# r = requests.get(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))
