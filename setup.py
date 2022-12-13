from setuptools import setup, find_packages 
with open("requirements.txt") as f:
    required_packages = f.readlines()

__version__ = "1.1.0"

setup(
   name='alerce',
   version=__version__",
   description='ALeRCE Client',
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=find_packages(),
   install_requires=required_packages,
)

