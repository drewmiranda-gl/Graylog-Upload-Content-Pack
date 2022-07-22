# pip install requests

import requests
from requests.auth import HTTPBasicAuth
import configparser

config = configparser.ConfigParser()
config.read('auth.ini')

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

sArgBuildUri=sArgBuildUri+sArgHost+":"+sArgPort

# ploads = {'things':2,'total':25}

# sUrl = "http://192.168.0.98:9000/api/messages/gl_linux_metricbeat_25/53da9da5-09ff-11ed-bd3c-000c291279c7"
sUrl = sArgBuildUri + "/api/messages/gl_linux_metricbeat_25/53da9da5-09ff-11ed-bd3c-000c291279c7"

sHeaders = {"Accept":"application/json"}

# params=ploads
# headers={"Content-Type":"text"}

r = requests.get(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))

# r = requests.post(sUrl, headers=sHeaders, verify=False, auth=HTTPBasicAuth(sArgUser, sArgPw))

print(r.status_code)
print(r.headers)
print(r.text)
# print(r.url)
