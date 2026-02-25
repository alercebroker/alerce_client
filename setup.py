from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = [r.strip() for r in f.readlines() if r.strip()]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

__version__ = "2.2.1"

setup(
    name="alerce",
    version=__version__,
    description="ALeRCE Client",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="ALeRCE Team",
    author_email="contact@alerce.online",
    packages=find_packages(),
    install_requires=required_packages,
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        "alerce": ["default_config.json"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries",
    ],
)
