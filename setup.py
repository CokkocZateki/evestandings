#!/usr/bin/env python
 
from setuptools import setup
from standings import __version__
 
setup(name="standings",
      version=__version__,
      description="EVE API Standings Page Generator",
      author="Andrew Williams",
      author_email="andy@tensixtyone.com",
      url="https://dev.pleaseignore.com/",
      keywords="eveapi",
      packages=['standings'],
      package_data={'standings': ['templates/*.html']},
      entry_points={
          'console_scripts': [
              'evestandings = standings.cli:main',
          ]
      },
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Development Status :: 3 - Alpha',
      ]
)
