# Doodle Dashboard

Doodle Dashboard is simple framework for creating a dashboard powered by [Slack](https://slack.com/).

I originally created the dashboard to display my bank balance on my [Raspberry Pi](https://www.raspberrypi.org/). 
Unfortunately the only way of knowing my balance without logging in to the bank's website was via a weekly SMS 
message they sent containing its balance, so using the automation app 
[Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) I was able to detect the SMS 
message, redirect it to a private Slack channel and have Doodle Dashboard extract the account balance and display it.


## Requirements

 * [Python 2.7](https://www.python.org/downloads/)
 * [pip](https://pip.pypa.io/en/stable/installing/)


## Building the project

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

## Starting the dashboard

```
$ cd doodle-dashboard
$ export PYTHONPATH=`pwd`
$ python doodledashboard/main.py <PATH TO CONFIG FROM STEP 4>
```


## Products that integrate with Slack

### Websites

* [Zapier](https://zapier.com/)
* [IFTTT](https://ifttt.com/)
* [Microsoft Flow](https://flow.microsoft.com/)

### Apps

* [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm)
