#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 08 Mar 2025 10:50:14 PM GMT
# scanner.py
# Description:
#  the scanner for the citrix instance

import requests, re
from bs4 import BeautifulSoup

try :
	from .webapi_linux import *
except:
	from webapi_linux import *

def get_customs(endpoint, verify=False):
	res = requests.get("https://" + endpoint, verify=verify)
	if res.status_code == 200:
		soup = BeautifulSoup(res.text, "html.parser")
		script_tag = soup.find("script", {"id": "customScript"})
		if script_tag and script_tag.string:
			data = "[!] https://"+endpoint+"\n"+script_tag.string + "\n"
			script_content = script_tag.string
			script_urls = re.findall(r"<script src=\"(.*?)\">", script_content)
			full_urls = [requests.compat.urljoin("https://" + endpoint, url) for url in script_urls]
			print(full_urls)
			for link in full_urls:
				res = requests.get(link, verify=verify)
				if res.status_code == 200:
					data += "[!] " + link + "\n" + res.text + "\n"
			return data
		else:
			return None
	else:
		return None

# TODO: Get citrix version
# TODO: Add pretty print section

if __name__ == "__main__":
	import sys
	import getpass
	import pprint

	ENDPOINT_URL=""
	uname = input("Citrix username (domain\\user) >> ")
	passwd = getpass.getpass("Citrixt account password >> ")
	session = requests.Session()

	data = get_customs(ENDPOINT_URL, verify=True)
	if data == None:
		print("Url offline!")
		sys.exit(-1)
	print("Custom Scripts:")
	print(data)
	remote_config = get_config(ENDPOINT_URL, session, verify=True)
	print("Citrix configuration:")
	pprint.pprint(remote_config)
	device_id = register_receiver(ENDPOINT_URL, session, remote_config, verify=True)
	if device_id == None:
		print("ERROR DEVICE ID IS NONE")
		sys.exit(1)
	creds={
		"user":uname,
		"pass":passwd
	}
	if login(ENDPOINT_URL, session, remote_config,creds=creds, verify=True):
		apps = get_app_list(ENDPOINT_URL, session, verify=True)
		print("Found %d citrix apps:" % len(apps))
		for app in apps:
			pprint.pprint(app)
	else:
		print("login failed!")
	auth_config = get_auth_config(ENDPOINT_URL, session, verify=True)
	print("Citrix auth types:")
	pprint.pprint(auth_config)
