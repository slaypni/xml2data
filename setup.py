from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='xml2data',
      version=version,
      description="a library for converting xml into native data",
      long_description="""\
xml2data is a library for converting xml into native data, according to css-like format.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='xml html native css selector convert parser',
      author='slaypni',
      author_email='punigumi@gmail.com',
      url='https://github.com/slaypni/xml2data',
      license='MIT',
      packages=find_packages(exclude=['xml2data', 'xml2data.testsuite']),
      test_suite='xml2data.testsuite.suite',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml',
          'cssselect',
          'chardet',
          'minimock'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
