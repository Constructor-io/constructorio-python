from setuptools import setup

setup(
        name="constructor-io",
        version="0.0.5",
        download_url='https://github.com/Constructor-io/constructorio-python'
                     '/tarball/0.0.5',
        license="MIT",
        description="Constructor.IO Python Client",
        author="Constructor.io",
        author_email="info@constructor.io",
        url="https://www.constructor.io",
        install_requires=[
            "requests==2.7.0",
            "vcrpy==1.11.1",
        ],
        packages=["constructor_io"]
    )
