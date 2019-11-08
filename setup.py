from setuptools import setup
with open("requirements.txt") as f:
    required_packages = f.readlines()

setup(
   name='alerce',
   version='0.2',
   description='Package to access to ALeRCE data',
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=['alerce'],  #same as name
   install_requires=required_packages, 

)

