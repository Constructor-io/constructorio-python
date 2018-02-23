from setuptools import setup

VERSION = "0.0.9"

setup(
    name="constructor-io",
    version=VERSION,
    download_url='https://github.com/Constructor-io/constructorio-python'
                 '/tarball/' + VERSION,
    license="MIT",
    description="Constructor.IO Python Client",
    author="Constructor.io",
    author_email="info@constructor.io",
    url="https://www.constructor.io",
    install_requires=[
        "requests==2.7.0",
        "vcrpy==1.11.1",
    ],
    packages=["constructor_io"],
    classifiers=[
        "Topic :: Internet",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)
