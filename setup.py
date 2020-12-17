# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    REQS = reqs_file.read()

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='scrapy_plus',
    version='1.0.5',
    packages=find_packages(exclude=["tests"]),
    install_requires=REQS,
    url='http://www.github.com/dotnetage/scrapy_plus',
    license='BSD',
    author='Ray',
    author_email='csharp2002@hotmail.com',
    description="scrapy 常用爬网必备工具包",
    long_description=README,
    long_description_content_type='text/markdown',
    zip_safe=False,
    platforms='any',
    keywords=('scrapy', 'crawl', 'redis', 'tor'),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'])
