# POC Anomaly detection

[![N|Bluekiri](https://cldup.com/dTxpPi9lDf.thumb.png)](http://bluekiri.com)

This project start from the need of detect multiple status metric signals, in realtime. to ahieve this Bluekiri decided to implement our own application for manage multiple signals at the same time in a very easy way. This project able us to listen and detect temporal series in realtime from kafka topics.



# Future Features!

  - Dashboard for administrate the anomaly detection project, this dashboard will be able to add new topics. 
  - New connectors to sniff new different feeds like elastic search


# Lets start!

##### Requirements:
* [Docker] - compose version 3+ (https://docs.docker.com/compose/install/#prerequisites)

##### Installation

Open a bash terminal and export a environment variable with your local host ip, this is necessary to set the kafka advertised host.

```sh
$ export IP_HOST=<your private ip address>
$ docker-compose up --build
```

### Emit messages

All feed messages must have the following format:
```json
{
    "application": "test1",
    "value": 1.5,
    "ts": "2018-03-16T07:10:15+00:00"
}
```
In the example the feed topic is named ( **feed** ) and the output kafka topic is named ( **predict**), this is only for the prove of concept, in the future, this will be changed dynamically.