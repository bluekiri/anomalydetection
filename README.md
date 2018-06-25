# Anomaly Detection Framework
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors)

![N|Bluekiri](var/bluekiri_logo.png?raw=true "Bluekiri")

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
    1. [Install](#install)
    2. [Input messages](#input-messages)
    3. [Run](#run)
    4. [Devel mode](#devel-mode)
3. [Use as Framework](#use-as-framework)
4. [Status](#status)
5. [Roadmap](#roadmap)
6. [License](#license)
7. [Contributors](#contributors)

## Documentation

TODO

## Getting started

### Install

1. Clone the repository

    ```bash
    git clone https://github.com/bluekiri/anomalydetection.git
    ```

2. Build and Run the demo will require some dependencies to be installed.

    System binaries
    
    - build-essential
    - python3
    - pip
    - virtualenvwrapper
    - nodejs
    - npm
    
    ```bash
    sudo apt-get install python3 python3-dev python3-pip nodejs npm build-essential
    sudo pip3 install virtualenvwrapper
    ```
    
    System libraries
    
    - libsasl2-dev
    - libldap2-dev
    - libssl-dev
    
    ```bash
    sudo apt-get install libsasl2-dev libldap2-dev libssl-dev
    ```

3. Create a virtualenv

    ```bash
    VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv --python=/usr/bin/python3 -a anomalydetection anomalydetection
    ```

4. Build

    It's required to run some tasks to get some JavaScript dependencies, download
    a Apache Spark distributable. These tasks are grouped in a Makefile
    
    ```bash
    make
    ```
     
### Input messages

At this moment, there is only one input message parser implementation, and all 
input messages must have the following JSON format:

```json
{
    "application": "test1",
    "value": 1.5,
    "ts": "2018-03-16T07:10:15+00:00"
}
```

You can check this implementation at [json_input_message_handler.py](src/anomalydetection/backend/entities/json_input_message_handler.py#29)
   
### Run

To run it using your own configuration you have to place a file ```anomdec.yml```
inside the ```anomdec``` path in user home directory.

```$HOME/anomdec/anomdec.yml```

Take [anomdec.yml](src/anomalydetection/anomdec.yml) as example config file.

Do the same with [logging.yml](src/anomalydetection/logging.yml) if you want
to overwrite the default settings of logging (Is in DEBUG level while developing).

And run it typing

```bash
export SPARK_HOME="<spark home directory>"
python3 -m anomalydetection.anomdec
```

### Devel mode

At this moment, there is a _devel_/_demo_ mode to demonstrate how the system works. It
generates multiple signals using kafka and pubsub as message systems. Then,
those messages are aggregated (or not) and processed by multiple models. At
last the result of these are displayed in realtime by the dashboard.

1. Install dependencies for docker

    - docker [howto](https://docs.docker.com/install/#supported-platforms)
    - docker-compose [howto](https://docs.docker.com/compose/install/)

2. Deploy a testing environment on docker

    This will deploy a kafka broker and a pubsub emulator to allow you to test
    the system.

    ```bash
    export HOST_IP="<host ip address>"
    docker-compose up --build
    ```

3. Run in devel mode

    You can run it as a python module

    ```bash
    export SPARK_HOME="<spark home directory>"
    python -m anomalydetection.anomdec devel
    ```
    
### Use as Framework

You can also use it as Framework to compose your own workflow and detect anomalies
anywhere you need.

```python
# -*- coding:utf-8 -*- #

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.backend.stream import \
    BaseStreamBackend, \
    BasePollingStream, \
    BasePushingStream
from anomalydetection.backend.engine.builder import BaseBuilder
from anomalydetection.backend.middleware.store_repository_middleware import  \
    StoreRepositoryMiddleware
from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.observable import ObservableRepository

class MyStreamInput(BasePollingStream):
    pass  # IMPLEMENT ME
    
class MyStreamOutput(BasePushingStream):
    pass  # IMPLEMENT ME

class MyStreamBackend(BaseStreamBackend):
    pass  # IMPLEMENT ME
    
class MyModelBuilder(BaseBuilder):
    pass  # IMPLEMENT ME
    
class MyRepository(BaseRepository):
    pass  # IMPLEMENT ME
    
class MyMessageHandler(BaseMessageHandler[InputMessage]):
    pass  # IMPLEMENT ME

interactor = StreamEngineInteractor(
    MyStreamBackend(MyStreamInput(), MyStreamOutput()),
    MyModelBuilder(),
    MyMessageHandler(),
    [StoreRepositoryMiddleware(MyRepository("file:///data/data.txt"))],
    ObservableRepository(MyRepository("file:///data/data.txt"))
)
interactor.run()

```

## Status

This project is in the earliest phase of its development. Use it under your
own responsibility.

## Roadmap

- [ ] Write tests.
- [ ] Write docs.
- [ ] Change some core architecture to enable processing a signal by multiple models.
- [ ] PubSub aggregate messages in Apache Spark.
- [ ] Implement a plugin engine.
- [ ] Persist configuration instead of use an static YAML file.
- [ ] ElasticSearch repository.

## License

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
    
## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
| [<img src="https://avatars0.githubusercontent.com/u/243109?v=4" width="100px;"/><br /><sub><b>David Martín :: Suki_ ::</b></sub>](http://sukiweb.net)<br />[🤔](#ideas-sukiweb "Ideas, Planning, & Feedback") | [<img src="https://avatars3.githubusercontent.com/u/6574210?v=4" width="100px;"/><br /><sub><b>Óscar</b></sub>](https://github.com/OscarGarciaPeinado)<br />[💻](https://github.com/bluekiri/anomalydetection/commits?author=OscarGarciaPeinado "Code") [🤔](#ideas-OscarGarciaPeinado "Ideas, Planning, & Feedback") | [<img src="https://avatars0.githubusercontent.com/u/1277789?v=4" width="100px;"/><br /><sub><b>Cristòfol Torrens</b></sub>](https://github.com/piffall)<br />[💻](https://github.com/bluekiri/anomalydetection/commits?author=piffall "Code") [📖](https://github.com/bluekiri/anomalydetection/commits?author=piffall "Documentation") [🤔](#ideas-piffall "Ideas, Planning, & Feedback") |
| :---: | :---: | :---: |
<!-- ALL-CONTRIBUTORS-LIST:END -->
Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!