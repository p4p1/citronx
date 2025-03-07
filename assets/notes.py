# THIS SCRIPT IS WHAT I USED FOR MY INITIAL TESTING NOT TO BE REUSED HERE FOR
# INFORMATION ONLY
import os
import requests
import base64, json

parameter_tool_launching_app="action=launch&serverProtocolVersion=1&transport=https&ticket="
parameter_tool_detect_device="action=detect&serverProtocolVersion=1&transport=https&ticket="
tool_path_windows="C:\\Program Files (x86)\\Citrix\\ICA Client\\WebHelper.exe"
domain="citrix.net"
citrix_endpoint="citrix.net/Citrix/Store"

res = requests.get("https://"+domain+"//", verify=False)
print(res.headers['Set-Cookie'])
cookies={"ns_csf-ha" : "ffffffff0988037f45525d5f4f58455e445a4a42378b"}
headers={"X-Citrix-Isusinghttps": "Yes"}

# STEP 1: initial setup before login

res = requests.post("https://"+citrix_endpoint+"/Home/Configuration", verify=False, cookies=cookies, headers=headers)
# You do not need to be logged in for that request and can just use it to get the info of the citrix setup
# this will return a xml config file

res = requests.post("https://"+citrix_endpoint+"/ClientAssistant/GetDetectionTicket", verify=False, cookies=cookies, headers=headers)
# this function will return a ticket and status as success this ticket need
# to then be sent to the next request
ticket = res.json()["clientDetectionTicket"]

os.system("\"%s\" \"receiver://%s/clientAssistant/reportDetectionStatus/%s\"" % (tool_path, citrix_endpoint, base64.b64encode(parameter_tool_detect_device.encode("ascii") + ticket.encode("ascii")).decode('ascii')))

res = requests.post("https://"+citrix_endpoint+"/ClientAssistant/GetDetectionStatus", data={"ticket": ticket}, verify=False, cookies=cookies, headers=headers)
# with the ticket sent to this you should then get the result status as true
# you can then request the following to get the ticket

res = requests.post("https://"+citrix_endpoint+"/Resources/List",verify=False, cookies=cookies, headers=headers)
# in this request you should see in the response the Set-Cookie with the device id
cookies={"ns_csf-ha" : "ffffffff0988037f45525d5f4f58455e445a4a42378b", "CtxsDeviceId": "WR_1EX3C6Lr6HTs"}



# STEP 2: login
res = requests.post("https://"+citrix_endpoint+"/Authentication/GetAuthMethods",verify=False, cookies=cookies, headers=headers)
# this will return the configuration of the server on how to login to citrix we are looking for ExplicitForms
# that will give you username and password login
cookies={"ns_csf-ha" : "", "CtxsDeviceId": "", "CsrfToken":"",
         "CtxsAuthMethod":"", "CtxsClientDetectionDone":"", "CtxsIsPassThrough":"", "CtxsClientVersion":"",
         "CtxsHasUpgradeBeenShown":"true", "ASP.NET_SessionId":""}
headers={"X-Citrix-Isusinghttps": "Yes", "Csrf-Token":""}


creds = {
"username":"CHANGE ME", # DONT FORGET TO EDIT THIS TOO
"password":"CHANGE ME", # DONT FORGET TO REPLACE
"saveCredentials": "false",
"loginBtn": "Log On",
"StateContext": ""
}
res = requests.post("https://"+citrix_endpoint+"/ExplicitAuth/LoginAttempt",verify=False, cookies=cookies, headers=headers, data=creds)
# this is the endpoint where you send the username and password and should return a xml
# with a success status to indicate login you need to make sure that the previous getAuthMethods is done quickly before the login request to work there is
# a short time window up until fail
print(res.headers["Set-Cookie"])
cookies={"ns_csf-ha" : "", "CtxsDeviceId": "", "CsrfToken":"",
         "CtxsAuthMethod":"", "CtxsClientDetectionDone":"true", "CtxsIsPassThrough":"false", "CtxsClientVersion":"",
         "CtxsHasUpgradeBeenShown":"true", "ASP.NET_SessionId":"", "CtxsAuthId": ""}


res = requests.post("https://"+citrix_endpoint+"/Resources/List", verify=False, cookies=cookies, headers=headers)
print (res.json()["resources"][0])
# using the previously gotten cookies you should now be able to list the installed applications
copy = res
# STEP 3: launch an app

appdata = {
    "displayNameDesktopTitle": copy.json()["resources"][1]['name'],
    "createFileFetchTicket": "true"
    }
res = requests.post("https://"+citrix_endpoint+ copy.json()["resources"][1]['launchstatusurl'], data=appdata,verify=False, cookies=cookies, headers=headers)
# this will create a ticket id for launching an application that you can then use in the following way:
ticket = res.json()["fileFetchTicket"]

print("\"%s\" \"receiver://%s/clientAssistant/getIcaFile/%s\"" % (tool_path, citrix_endpoint, base64.b64encode(parameter_tool_launching_app.encode('ascii') + ticket.encode('ascii')).decode('ascii')))

