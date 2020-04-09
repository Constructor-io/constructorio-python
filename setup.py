from setuptools import setup
from pip._internal.req import parse_requirements

VERSION = "0.0.11"

requirements_py3 = [str(r.req) for r in parse_requirements('requirements.txt', session=False)]
requirements_py2 = [str(r.req) for r in parse_requirements('requirements-py2.txt', session=False)]
install_requires = [
    '%s; python_version>="3"' % req for req in requirements_py3
] + [
    '%s; python_version<"3"' % req for req in requirements_py2
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
