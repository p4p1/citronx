#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Fri 07 Mar 2025 11:26:16 AM GMT
# webapilinux.py
# Description:
#  use the webapi of citrix with this tool on linux

import os, time,sys
import requests, xmltodict, base64
import urllib.parse

def is_online(endpoint, session, verify=False):
	res = session.get("https://" + endpoint, verify=verify)
	if res.status_code == 200:
		return True
	else:
		return False

def get_config(endpoint, session, verify=False):
	session.headers.update({
		"X-Citrix-Isusinghttps": "Yes"
	})
	res = session.post("https://" + endpoint + "/Home/Configuration", verify=verify)
	if res.status_code == 200:
		return xmltodict.parse(res.text)
	else:
		return None

def get_auth_config(endpoint, session, verify=False):
	res = session.post("https://" + endpoint + "/Authentication/GetAuthMethods", verify=verify)
	if res.status_code == 200:
		return xmltodict.parse(res.text)
	else:
		return None

def get_app_list(endpoint, session, verify=False):
	remote_config = get_config(endpoint, session)
	if remote_config == None:
		print("error")
		return None
	uri = remote_config["clientSettings"]["storeProxy"]["resourcesProxy"]["@listURL"]
	res = session.post("https://" + endpoint + uri, verify=verify)
	if res.status_code == 200:
		return res.json()["resources"]
	else:
		return None

def launch_app(endpoint, session, app, verify=False):
	parameter_tool_launching_app="action=launch&serverProtocolVersion=1&transport=https&ticket="

	appdata = {
		"displayNameDesktopTitle": app['name'],
		"createFileFetchTicket": "true"
	}
	uri = app['launchstatusurl']
	res = session.get("https://" + endpoint + "/" + app['launchurl'] +
				f"?CsrfToken={session.cookies['CsrfToken']}&IsUsingHttps=Yes&displayNameDesktopTitle={urllib.parse.quote(app['name'])}",
				verify=verify, data=appdata)
	with open('/tmp/tmp.ica', 'w') as fp:
		fp.write(res.text)

	os.system("/home/p4p1/Documents/github/citronx/assets/linuxx64/wfica.sh /tmp/tmp.ica")



def register_receiver(endpoint, session, remote_config, verify=False):
	session.headers.update({
		"Csrf-Token":session.cookies["CsrfToken"]
	})
	cookies={"CtxsUserPreferredClient":"Native", "CtxsClientDetectionDone":"true", "CtxsHasUpgradeBeenShown":"true"}
	uri = remote_config["clientSettings"]["storeProxy"]["resourcesProxy"]["@listURL"]
	data={"format":"json","resourceDetails":"Default"}

	res = session.post("https://" + endpoint + uri, verify=verify, cookies=cookies, data=data)
	if res.status_code == 200:
		return res.cookies["CtxsDeviceId"]
	else:
		return None

def login(endpoint, session, remote_config, creds={"user":"bob","pass":"bob"}, verify=False):
	auth_config = get_auth_config(endpoint, session)
	uri = next(m['@url'] for m in auth_config['authMethods']['method'] if m['@name'] == 'ExplicitForms')
	res = session.post("https://" + endpoint + "/" + uri, verify=verify)

	# TODO: add verificatoin of res.xml.explicit aut

	form = {
		"username":creds["user"], # DONT FORGET TO EDIT THIS TOO
		"password":creds["pass"], # DONT FORGET TO REPLACE
		"saveCredentials": "false",
		"loginBtn": "Log On",
		"StateContext": ""
	}

	res = session.post("https://" + endpoint + "/ExplicitAuth/LoginAttempt", verify=verify, data=form)

	if "CtxsAuthId" in res.headers['Set-Cookie']:
		return True
	else:
		return False

if __name__ == "__main__":
	import getpass

	# the test of the webapi with an example web store
	ENDPOINT_URL="" # REAPLACE HERE WITH THE URL NEEDED
	uname = input("Citrix username (domain\\user) >> ")
	passwd = getpass.getpass("Citrixt account password >> ")
	session=requests.Session()

	if is_online(ENDPOINT_URL, session):
		remote_config = get_config(ENDPOINT_URL, session)
		device_id = register_receiver(ENDPOINT_URL, session, remote_config)
		if device_id == None:
			print("ERROR DEVICE ID IS NONE")
			sys.exit(1)
		creds={
			"user":uname,
			"pass":passwd
		}
		if login(ENDPOINT_URL, session, remote_config,creds=creds):
			apps = get_app_list(ENDPOINT_URL, session)
			print("found %d apps:" % len(apps))
			for app in apps:
				print(app["name"])
			while (n := input(f"Enter a number between 0 and {len(apps)-1}: ")).isdigit() and 0 <= (n := int(n)) < len(apps):
				launch_app(ENDPOINT_URL, session, apps[n])
