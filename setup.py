from distutils.core import setup
from my_python import PARENT_PATH, VERSION, py_modules, license_text


setup(name=PARENT_PATH.name,
      version=VERSION,
      py_modules=py_modules(),
      license=license_text(),
      )
