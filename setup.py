#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools
with open('README.md', 'r') as readme:
    README_TEXT = readme.read()

setuptools.setup(
    name='jsontocsv',
    version='1.0',
    description='Easy-way to parser nested json <--> csv file.',
    long_description = README_TEXT,
    long_description_content_type='text/markdown',
    author='Elison Márcio Correa',
    author_email='marcioinfo.correa@gmail.com',
    url='https://github.com/marcioinfo/PositionalFilesReader',
    install_requires=['six'],
    license='BSD',
    keywords='JSON To CSV',
    test_suite="jsontocsv.tests",
    classifiers=[],
)
