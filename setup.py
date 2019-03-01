# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    REQS = reqs_file.read()

setup(
    name='scrapy_plus',
    version='1.0',
    package_dir={'': 'scrapy_plus'},
    packages=find_packages('scrapy_plus'),
    install_requires=REQS,
    url='http://www.github.com/dotnetage/scrapy_plus',
    license='BSD',
    author='Ray',
    author_email='csharp2002@hotmail.com',
    description="scrapy 常用爬网必备工具包",
    zip_safe=False,
    platforms='any',
    keywords=('scrapy', 'crawl', 'redis', 'tor'),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: Chinese',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'])
