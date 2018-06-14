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

from setuptools import find_packages, setup

install_require = [
    # Core dependencies
    "rx", "jsonschema", "python-dateutil",
    "numpy", "pandas", "statsmodels", "bokeh",
    # Kafka
    "kafka-python",
    # Google api base
    "oauth2client", "google-auth", "google-auth-httplib2",
    "google-api-python-client",
    # Google cloud base
    "google-cloud", "google-cloud-pubsub",
    # Dashboard
    "tornado", "PyYAML", "python-ldap", "websockets"
]

test_require = [
    "mock",
    "coverage",
    "nose",
    "tox"
]

setup(
    name='anomdec',
    version='0.0.0',
    description='Anomaly detection bridge',
    url='',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages('src', exclude=("test", "test.*")),
    package_dir={'': 'src'},
    install_requires=install_require,
    test_suite="nose.collector"
)
