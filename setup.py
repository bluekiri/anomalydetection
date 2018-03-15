#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import find_packages, setup
import io
import re
import glob
from os.path import join
from os.path import dirname
from os.path import splitext
from os.path import basename


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='poc-anomaly-detection',
    version='0.0.0',
    description='POC anomaly detection',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    url='',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages('src', exclude=("tests", "tests.*")),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob.glob('src/*.py')],
    classifiers=[
        'Programming Language :: Python :: 3.5.2',
        'Operating System :: Unix',
    ],
    install_requires=[
        "kafka-python"
    ]
)
