from setuptools import setup
from pkg_resources import parse_requirements

VERSION = "0.0.11"

with open('requirements.txt', 'r') as f:
    requirements = list(map(str, parse_requirements(f)))

with open('requirements-py2.txt', 'r') as f:
    extra_py2_requirements = list(map(str, parse_requirements(f)))

install_requires = requirements + [
    '%s; python_version<"3"' % req for req in extra_py2_requirements
]

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
    install_requires=install_requires,
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
