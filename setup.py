from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='droit',
	version='1.1.2',
	description='Simple library for creating bots',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/jarinox/python-droit',
	author='Jakob Stolze',
	author_email='jarinox@wolke7.de',
	license='LGPLv2.1',
	packages=['droit'],
	install_requires=['parse'],
	include_package_data=True,
	python_requires='>=3.6',
	zip_safe=False
)
