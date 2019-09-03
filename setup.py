from setuptools import setup

setup(
   name='alerce',
   version='0.1',
   description='Package to access to ALeRCE data',
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=['alerce'],  #same as name
   install_requires=['pandas', 'requests', 'IPython'], #external packages as dependencies
)

