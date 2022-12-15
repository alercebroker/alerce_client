from setuptools import setup, find_packages 
with open("requirements.txt") as f:
    required_packages = f.readlines()
  
# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "1.2.0"

setup(
   name='alerce',
   version=__version__,
   description='ALeRCE Client',
   long_description_content_type="text/markdown",
   long_description=long_description,
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=find_packages(),
   install_requires=required_packages,
)

