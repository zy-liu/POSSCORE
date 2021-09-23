# -*- coding:utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name = 'posscore',
      version = '0.0.1',
      packages = find_packages(where='./src/'),  
      package_dir = {'':'src'}, 
      include_package_data = False,
      package_data = {'data':[]},
      description = 'This is a package for the POSSCORE metric.',
      long_description = long_description,
      long_description_content_type="text/markdown",
      author = 'Zeyang Liu',
      author_email = 'liuzeyang0001@gmail.com',
      url = 'https://github.com/zy-liu/POSSCORE',  # homepage
      install_requires = [
            'nltk>=3.4.3',
            'gensim>=3.8.0',
            'numpy',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
     )