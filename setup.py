from setuptools import setup

setup(
	name="citronx",
	version='0.0.1',
	description='a python tool to pentest citrix web apps',
	url="",
	author='p4p1',
	license='GPL V3',
	packages=['citronx'],
	install_requires=[
		"requests",
		"beautifulsoup4",
		"textual"
	],
	scripts=['bin/citronx'],
	zip_safe=False
)
