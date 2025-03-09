#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 08 Mar 2025 07:19:01 PM GMT
# gui.py
# Description:
#  The citronx user interface to view clients and their apps in textual

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Label
from textual.containers import Container

try :
	from .webapi_linux import *
except:
	from webapi_linux import *

class UserRow(Static):
	""" display a user row """

	def __init__(self, appdata:list, config:dict, session) -> None:
		super().__init__()
		self.appdata = appdata
		self.config = config
		self.session = session

	def compose(self) -> ComposeResult:
		yield Button(f"{self.appdata["name"]}", classes="dracula-button")

	def on_button_pressed(self, event:Button.Pressed) -> None:
		self.notify(f"Launching: {self.appdata['name']}")
		if "fakeurl" not in self.config["server"]:
			launch_app(self.config["server"], self.session, self.appdata, self.config["run_ica"], verify=self.config["secure"])

class Citronx(App[str]):
	TITLE = "Citronx"
	SUBTITLE = "A citrix scanner"
	CSS = """
	Screen {
		layout: vertical;
		background: rgb(40, 42, 54);
		color: rgb(248, 248, 242);
	}
	Container.row {
		width: 100%;
		height: 10;
		layout: horizontal;
		overflow-x: auto;
		border: solid rgb(98, 114, 164);
	}
	Button {
		width: 100%;
		height:100%;
	}
	Static {
		width: 30;
		height: 100%;
		margin: 1;
		background: rgb(68, 71, 90);
		color: rgb(248, 248, 242);
		text-align: center;
		border: solid white;
	}
	.dracula-button {
		background: rgb(189, 147, 249);
		color: rgb(40, 42, 54);
		border: solid rgb(80, 250, 123);
	}
	.dracula-button:hover {
		background: rgb(80, 250, 123);
		color: rgb(40, 42, 54);
		border: solid rgb(189, 147, 249);
	}
	Label {
		height: 2;
		border: none;
	}
	"""

	def __init__(self, citrix_data:list, config:dict) -> None:
		super().__init__()
		self.citrix_data = citrix_data
		self.config = config

	def compose(self) -> ComposeResult:
		yield Header()
		for user in self.citrix_data:
			yield Label(f"{user["username"]}")
			with Container(classes="row"):
				for app in user['apps']:
					yield UserRow(appdata=app, config=self.config, session=user["session"])

if __name__ == "__main__":
	fake_config = {
		"server": "fakeurl"
	}
	fake_citrix_data = [
		{
			'username':'domain\\user1',
			'session': 'requests.Session()',
			'apps': [
				{
					"name": "Online Desktop",
					"url": "user1/firsturl"
				},
				{
					"name": "Excel Corporate",
					"url": "user2/secondurl"
				}
			]
		},
		{
			'username': 'domain\\user2',
			'session': 'requests.Session()',
			'apps': [
				{
					"name": "Online Desktop",
					"url": "user2/coolurl"
				},
				{
					"name": "Sample Finance",
					"url": "user2/secondurl"
				},
				{
					"name": "qrst",
					"url": "user2/thirdurl"
				},
				{
					"name": "uvwx",
					"url": "user2/fourthurl"
				}
			]
		}
	]
	app = Citronx(citrix_data=fake_citrix_data, config=fake_config)
	reply = app.run()
