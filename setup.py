# -*- encoding: utf-8 -*-
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import os

from setuptools import find_packages, setup


def _read_from_file(_file):
    try:
        _file = os.path.join(os.path.dirname(__file__), _file)
        return open(_file, 'r').read().strip().split('.')
    except Exception as _:
        return []


VERSION = _read_from_file('version.info')
BUILD = _read_from_file('build.info')

__version__ = '.'.join([str(v) for v in VERSION + BUILD])

install_require = [
    # Core dependencies
    "Rx==1.6.1", "jsonschema==2.6.0", "python-dateutil==2.1", "scipy==1.1.0",
    "numpy==1.14.2", "pandas==0.22.0", "statsmodels==0.8.0", "bokeh==0.12.16",
    # Kafka
    "kafka-python==1.4.2",
    # Google api base
    "oauth2client==2.0.0", "google-auth==1.5.0", "google-auth-httplib2==0.0.3",
    "google-api-python-client==1.7.3",
    # Google cloud base
    "google-cloud==0.33.1", "google-cloud-pubsub==0.30.0",
    # Dashboard
    "tornado==5.0.2", "PyYAML==3.12", "python-ldap==3.0.0", "websockets==5.0.1",
    # Spark
    "findspark==1.3.0"
]

# Avoid installation of dependencies in RTD, and install
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    install_require = []

test_require = [
    "mock",
    "coverage",
    "nose",
    "tox"
]

setup(
    name='anomalydetection',
    version=__version__,
    description='Anomaly detection bridge',
    url='',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages('src', exclude=("test", "test.*")),
    package_dir={'': 'src'},
    install_requires=install_require,
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        # Status
        'Development Status :: 2 - Pre-Alpha',
        # License
        'License :: OSI Approved :: GNU Affero General Public License v3',
        # Python
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        # SO
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        # Environment
        'Environment :: Web Environment',
        # Topics
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    test_suite="nose.collector",
    entry_points={
        'console_scripts': [
            'anomdec=anomalydetection.anomdec:main'
        ]
    }
)
