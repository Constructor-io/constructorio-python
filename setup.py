import os

from setuptools import find_packages, setup

from constructor_io import __version__

this_directory = os.path.dirname(os.path.abspath(__file__))
long_description_path = os.path.join(this_directory, "README.md")

with open(long_description_path, "r") as long_description_file: # pylint: disable=unspecified-encoding
    long_description = long_description_file.read()

setup(
    name="constructor-io",
    version=__version__,
    download_url='https://github.com/Constructor-io/constructor-io/tarball/' + __version__,
    license="MIT",
    description="Constructor.IO Python Client",
    author="Constructor.io",
    author_email="info@constructor.io",
    url="https://www.constructor.io",
    install_requires=[
        'requests~=2.26'
    ],
    packages = find_packages(exclude=["tests.*", "tests"]),
    long_description=long_description,
    long_description_content_type='text/markdown',
)
