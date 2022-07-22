from setuptools import setup, find_packages
from my_python import PARENT_PATH, VERSION, license_text


setup(name=PARENT_PATH.name,
      version=VERSION,
      packages=find_packages(),
      license=license_text(),
      )
