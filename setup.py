from pathlib import Path

from setuptools import find_packages, setup

from constructor_io import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

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
