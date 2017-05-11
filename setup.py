#!/usr/bin/env python
from setuptools import setup, find_packages
__author__ = 'adamkoziol'

setup(
    name="ftir_renamer",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    author='Adam Koziol',
    author_email='adam.koziol@inspection.gc.ca',
    description='File renamer for FTIR files',
    url='https://github.com/adamkoziol/ftir_renamer.git',
    long_description=open('README.md').read(),
    install_requires=['pandas',
                      'xlrd'],
)
