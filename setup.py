from setuptools import find_packages, setup

VERSION = "1.0.0"


setup(
    name="constructor-io",
    version=VERSION,
    download_url='https://github.com/Constructor-io/constructor-io/tarball/' + VERSION,
    license="MIT",
    description="Constructor.IO Python Client",
    author="Constructor.io",
    author_email="info@constructor.io",
    url="https://www.constructor.io",
    install_requires=[
        'requests~=2.26'
    ],
    packages=find_packages(exclude=("tests",)),
)
