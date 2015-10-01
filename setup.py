from distutils.core import setup

setup(
        name="constructor-io",
        version="0.0.1",
        description="Constructor.IO Python Client",
        author="Howon Lee",
        author_email="howon@constructor.io",
        url="https://www.constructor.io",
        install_requires=[
            "requests",
            "vcrpy"
        ],
        packages=["constructor_io"]
    )
