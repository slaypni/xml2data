from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='xml2data',
      version=version,
      description="a html parser with json like css selector",
      long_description="""\
json like parser""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='css json html parser',
      author='Kazuaki Tanida',
      author_email='punigumi@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['xml2data', 'xml2data.testsuite']),
      test_suite='xml2data.testsuite.suite',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
