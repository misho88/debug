#!/usr/bin/env python3

import setuptools

import debug
long_description = debug.__doc__

setuptools.setup(
    name='debug',
    version='0.0.1',
    author='Mihail Georgiev',
    author_email='misho88@gmail.com',
    description='print-like function for debugging',
    long_description=long_description,
    long_description_content_type='text/plain',
    url='https://github.com/misho88/debug',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    py_modules=['debug']
)
