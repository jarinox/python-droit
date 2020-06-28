from setuptools import setup

setup(
	name='droit',
	version='1.0.1',
	description='Simple library for creating bots',
	url='https://github.com/jarinox/python-droit',
	author='Jakob Stolze',
	author_email='jarinox@wolke7.de',
	licence='LGPLv2.1',
	packages=['droit', 'droit.io'],
	install_requires=['parse'],
	include_package_data=True,
	zip_safe=False
)
