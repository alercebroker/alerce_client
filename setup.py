from setuptools import setup, find_packages
with open("requirements.txt") as f:
    required_packages = f.readlines()

exec(
    compile(open("alerce/__init__.py").read(), "alerce/__init__.py", "exec")
)

setup(
   name='alerce',
   version=__version__,
   description=__description__,
   author='ALeRCE Team',
   author_email='contact@alerce.online',
   packages=find_packages(),
   install_requires=required_packages,
)
