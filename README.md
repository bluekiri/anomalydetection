# Anomaly Detection Framework

![N|Bluekiri](var/bluekiri_logo.png?raw=true "Bluekiri")

This project born from the need of detect anomalies on multiple signals.
To achieve this, Bluekiri decided to implement its own system to manage
multiple signals at the same time in a easy and scalable way.

## Documentation

TODO

## Devel mode

At this moment, there is a _devel_/_demo_ mode to demonstrate how the system works. It
generates multiple signals using kafka and pubsub as message systems. Then,
those messages are aggregated (or not) and processed by multiple models. At
last the result of these are displayed in realtime by the dashboard.

## Set Up

1. Clone the repository

    ```bash
    git clone https://github.com/bluekiri/anomalydetection.git
    ```

2. Build and Run the demo will require some dependencies to be installed.

    System binaries
    
    - docker [howto](https://docs.docker.com/install/#supported-platforms)
    - docker-compose [howto](https://docs.docker.com/compose/install/)
    - python3
    - pip
    - virtualenvwrapper
    - make
    - nodejs
    - npm
    
    ```bash
    sudo apt-get install python3 python3-dev python3-pip nodejs npm
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

5. Deploy a testing environment on docker

    This will deploy a kafka broker and a pubsub emulator to allow you to test
    the system.

    ```bash
    export HOST_IP="<host ip address>"
    docker-compose up --build
    ```

## Run in devel mode

You can run it as a python module

```bash
export SPARK_HOME="<spark home directory>"
python -m anomalydetection.anomdec devel
```
    
## Run in normal mode

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

## Message format

All feed messages must have the following JSON format:

```json
{
    "application": "test1",
    "value": 1.5,
    "ts": "2018-03-16T07:10:15+00:00"
}
```

## Status

This project is in the earliest phase of its development. Use it under your
own responsibility.

## TODO

* Change design to enable processing a signal by multiple models.
* Put configuration in MongoDB instead of a yaml file.
* ElasticSearch integration.
* PubSub aggregate messages.
* ...

# License

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