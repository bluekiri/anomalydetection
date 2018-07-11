# Anomaly Detection Framework

[![Build Status](https://travis-ci.org/bluekiri/anomalydetection.svg?branch=master)](https://travis-ci.org/bluekiri/anomalydetection)
[![codecov](https://codecov.io/gh/bluekiri/anomalydetection/branch/master/graph/badge.svg)](https://codecov.io/gh/bluekiri/anomalydetection)
[![Documentation](https://readthedocs.org/projects/anomalydetection/badge/?version=latest)](http://anomalydetection.readthedocs.io/)
[![All Contributors](https://img.shields.io/badge/all_contributors-4-blue.svg)](#contributors)

![N|Bluekiri](var/bluekiri_logo.png "Bluekiri")

## Overview

This project born from the need of detect anomalies on multiple signals.
To achieve this, Bluekiri decided to implement its own system to manage
multiple signals at the same time in a easy and scalable way.

## Architecture

This project uses Tornado, RxPy, Apache Spark and WebSockets to aggregate
and process streams of signals to detect anomalies and display it live on 
a dashboard.

## Table of content

1. [Documentation](#documentation)
2. [Getting started](#getting-started)
3. [License](#license)
4. [Contributors](#contributors)

## Documentation

You can read the documentation at [anomalydetection.readthedocs.io](http://anomalydetection.readthedocs.io/)

## Getting started

Please visit the Anomaly Detection Framework Documentation for help with
[Install](http://anomalydetection.readthedocs.io/en/latest/getting-started.html#install),
[Configuration](http://anomalydetection.readthedocs.io/en/latest/configuration.html) or
read how to [Deploy](http://anomalydetection.readthedocs.io/en/latest/deploy.html) each 
individual component. You can also find how to extend the Framework via 
[Plugins](http://anomalydetection.readthedocs.io/en/latest/plugins.html) to adapt to your
needs

## License

```txt
Anomaly Detection Framework
Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
    
## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
| [<img src="https://avatars0.githubusercontent.com/u/243109?v=4" width="100px;"/><br /><sub><b>David Martín :: Suki_ ::</b></sub>](http://sukiweb.net)<br />[🤔](#ideas-sukiweb "Ideas, Planning, & Feedback") | [<img src="https://avatars3.githubusercontent.com/u/6574210?v=4" width="100px;"/><br /><sub><b>Óscar</b></sub>](https://github.com/OscarGarciaPeinado)<br />[💻](https://github.com/bluekiri/anomalydetection/commits?author=OscarGarciaPeinado "Code") [🤔](#ideas-OscarGarciaPeinado "Ideas, Planning, & Feedback") | [<img src="https://avatars0.githubusercontent.com/u/1277789?v=4" width="100px;"/><br /><sub><b>Cristòfol Torrens</b></sub>](https://github.com/piffall)<br />[💻](https://github.com/bluekiri/anomalydetection/commits?author=piffall "Code") [📖](https://github.com/bluekiri/anomalydetection/commits?author=piffall "Documentation") [🤔](#ideas-piffall "Ideas, Planning, & Feedback") | [<img src="https://avatars1.githubusercontent.com/u/20190664?v=4" width="100px;"/><br /><sub><b>juan huguet</b></sub>](https://github.com/juanhuguetgarcia)<br />[💻](https://github.com/bluekiri/anomalydetection/commits?author=juanhuguetgarcia "Code") [🤔](#ideas-juanhuguetgarcia "Ideas, Planning, & Feedback") |
| :---: | :---: | :---: | :---: |
<!-- ALL-CONTRIBUTORS-LIST:END -->
Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!