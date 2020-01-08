from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pylaunch',
    py_modules=['dial','ssdp'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'':'src'},
    version='0.0.99',
    url='https://github.com/Sandersland.dial',
    author="Steffen Andersland",
    author_email='stefandersland@gmail.com',
    keywords=['dial'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ]
)