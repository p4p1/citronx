#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Fri 07 Mar 2025 09:02:27 PM GMT
# config.py
# Description:
#  handle the config file of citronx
#{
#	"server":"",
#	"users": [
#		{
#			"username": "",
#			"password": ""
#		}
#	]
#}

import json, os
import getpass

DEFAULT_CFG=os.environ["HOME"] + "/.config/citronx/config.json"

def create_config():
	conf_file = os.environ["HOME"] + "/.config/citronx/config.json"
	os.mkdir(os.environ["HOME"] + "/.config/citronx")
	url = input("domain + uri of citrix web: ")
	uname = input("username (domain\\user): ")
	passwd = getpass.getpass("password: ")
	run_ica = input("Path to the citrix binary running the ica files (wfica.sh): ")
	conf_data = {
		"server":url,
		"run_ica": run_ica,
		"secure": True,
		"users": [
			{
				"username": uname,
				"password": passwd
			}
		]
	}
	with open(conf_file, "w") as fp:
		json.dump(conf_data, fp, indent=4)

def load_config(path=DEFAULT_CFG):
	with open(path, "r") as fp:
		return json.load(fp)

if __name__ == "__main__":
	default = os.environ["HOME"] + "/.config/citronx/config.json"
	if not os.path.exists(default):
		create_config()
	print(load_config())
