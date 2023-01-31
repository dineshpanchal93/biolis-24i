from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in biolis24i/__init__.py
from biolis24i import __version__ as version

setup(
	name="biolis24i",
	version=version,
	description="sql server 2005 biolis 24i connection patient data",
	author="biolis",
	author_email="biolis@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
