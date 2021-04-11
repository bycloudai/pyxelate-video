#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='pyxelate',
      version='2.0.2',
      description='Pyxelate is a Python class that converts images into 8-bit pixel art.',
      url='http://github.com/sedthh/pyxelate',
      author='sedthh',
      license='MIT',
      packages=['pyxelate'],
      zip_safe=False,
      install_requires=[
          'scikit-learn>=0.24.1', 'scikit-image>=0.18.1'
      ],
      )
