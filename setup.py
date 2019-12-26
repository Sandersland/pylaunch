from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dial',
    packages=['dial'],
    description=long_description,
    version='0.0.4',
    url='https://github.com/Sandersland.dial',
    author="Steffen Andersland",
    author_email='stefandersland@gmail.com',
    keywords=['dial']
)