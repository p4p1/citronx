#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 08 Mar 2025 10:50:14 PM GMT
# scanner.py
# Description:
#  the scanner for the citrix instance

import requests

def get_customs(endpoint):
	res = requests.get("https://" + endpoint + "/custom/script.js", verify=verify)
	if res.status_code == 200:
		return res.text
	else:
		return None

# 1. Get citrix version
# 2. Extract all the custom citrix code from the frontend
# 3. List all the xml configs provided by the api
# 3.1 endpoints
# 3.2 auth type
# 4. list all apps from provided users

if __name__ == "__main__":
	ENDPOINT_URL=""
	print("Custom Scripts:")
	print(get_customs(url))
