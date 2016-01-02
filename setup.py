from distutils.core import setup

setup(
        name="constructor-io",
        version="0.0.3",
        license="MIT",
        description="Constructor.IO Python Client",
        author="Constructor.io",
        author_email="info@constructor.io",
        url="https://www.constructor.io",
        install_requires=[
            "requests",
            "vcrpy"
        ],
        packages=["constructor_io"]
    )
