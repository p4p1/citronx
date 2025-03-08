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
from webapi_linux import *

class UserRow(Static):
	""" display a user row """

	def __init__(self, appdata:list) -> None:
		super().__init__()
		self.appdata = appdata

	def compose(self) -> ComposeResult:
		yield Button(f"{self.appdata["name"]}", id=self.appdata['name'], classes="dracula-button")

	def on_button_pressed(self, event:Button.Pressed) -> None:
		self.notify(f"i pressed {self.appdata['url']}")

class Citronx(App[str]):
	TITLE = "Citronx"
	SUBTITLE = "A citrix scanner"
	CSS_PATH = "style/gui.tcss"

	def __init__(self, citrix_data:list) -> None:
		super().__init__()
		self.citrix_data = citrix_data

	def compose(self) -> ComposeResult:

		yield Header()
		for user in self.citrix_data:
			yield Label(f"{user["username"]}")
			with Container(classes="row"):
				for app in user['apps']:
					yield UserRow(appdata=app)

if __name__ == "__main__":
	fake_citrix_data = [
		{
			'username':'domain\\user1',
			'apps': [
				{
					"name": "abcd",
					"url": "user1/firsturl"
				},
				{
					"name": "efgh",
					"url": "user2/secondurl"
				}
			]
		},
		{
			'username': 'domain\\user2',
			'apps': [
				{
					"name": "ijkl",
					"url": "user2/coolurl"
				},
				{
					"name": "mnop",
					"url": "user2/secondurl"
				}
			]
		}
	]
	app = Citronx(citrix_data=fake_citrix_data)
	reply = app.run()
