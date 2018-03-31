# Doodle Dashboard [![Build Status](https://travis-ci.org/SketchingDev/Doodle-Dashboard.svg?branch=master)](https://travis-ci.org/SketchingDev/Doodle-Dashboard)

Doodle Dashboard is used to create fun little dashboards that display useful information from multiple sources, like
Tweets from your favourite Twitterers, weather reports for your local area or breaking news.

![High level diagram of messages flowing through framework](docs/images/flow-diagram.png?raw=true)

## Requirements
  * [Python 2.7](https://www.python.org/downloads/)
  * [pip](https://pip.pypa.io/en/stable/installing/)

## Getting started

  1. Start by reading [how to create the configuration file]() for your dashboard
  2. Install the requirements in the previous section
  3. Install Doodle-Dashboard
```
$ pip install doodle-dashboard
```
  4. Start the dashboard
```
$ doodledashboard <ABSOLUTE PATH TO YAML CONFIGURATION>
```

### Supported sources
  * [RSS](http://www.whatisrss.com/)
  * [Slack](https://slack.com/)

### Supported displays
  * [Papirus](https://uk.pi-supply.com/products/papirus-epaper-eink-screen-hat-for-raspberry-pi)


## Development

1. Clone the repository
```
$ git clone <PROJECT URL>
$ cd doodle-dashboard
```

2. Install project dependencies
```
$ make dev
```
or
```
$ pip install -r requirements.txt
$ pip install -r requirements.testing.txt
```

3. Running locally
```
$ export PYTHONPATH=`pwd`
$ python doodledashboard/main.py <ABSOLUTE PATH TO CONFIG FILE>
```

### ImportError: No module named

If you keep getting the ImportError when building the project check that you
haven't already installed the application via PIP, otherwise you might be pulling
in the doodle dashboard classes from your local pip packages.

```
sudo rm -rf /Library/Python/2.7/site-packages/doodledashboard/
```
