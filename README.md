# Doodle Dashboard [![Build Status](https://travis-ci.org/SketchingDev/Doodle-Dashboard.svg?branch=master)](https://travis-ci.org/SketchingDev/Doodle-Dashboard)

Doodle Dashboard is a highly extensible dashboard designed to display data from multiple sources. It was designed
with the Raspberry Pi in mind, though will work on any device that supports Python 2.7. 


## How it works

![High level diagram of messages flowing through framework](docs/images/flow-diagram.png?raw=true)

The dashboard works using the following elements:

 * **Data Source** - The external sources of information you want to display on the dashboard
 * **Filters** - Filters items from data sources based on customisable criteria
 * **Handler** - Draws information from the filtered items to the display
 * **Display** - The display attached to the device

The workings of the dashboard can be summarised by looking at how to display the latest weather:

1. Data Source - Configure the dashboard to poll the BBC's weather RSS feed
2. Filtering - Keep items from previous step that contain the text 'weather' 
3. Handler - Using items from previous step draw the relevant image to the dashboard based on the presence of the 
keyword of 'rain', 'sun', 'cloud' or 'storm'


## Configuration

[TODO]


## Requirements

 * [Python 2.7](https://www.python.org/downloads/)
 * [pip](https://pip.pypa.io/en/stable/installing/)


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

3. Create a configuration file
```
[Slack]
Token=<SLACK API TOKEN>
Channel=<NAME OF SLACK CHANNEL>
```

### ImportError: No module named

If you keep getting the ImportError when building the project check that you
haven't already installed the application via PIP, otherwise you might be pulling
in the doodle dashboard classes from your local pip packages.

```
sudo rm -rf /Library/Python/2.7/site-packages/doodledashboard/
```

## Starting the dashboard

```
$ cd doodle-dashboard
$ export PYTHONPATH=`pwd`
$ python doodledashboard/main.py <PATH TO CONFIG FROM STEP 4>
```
