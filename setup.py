from setuptools import setup, find_packages 
with open("requirements.txt") as f:
    required_packages = f.readlines()

setup(
   name='alerce',
   version="1.0.0",
   description='ALeRCE Client',
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=find_packages(),
   install_requires=required_packages,
)

