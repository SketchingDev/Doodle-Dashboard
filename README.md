# Doodle Dashboard

Doodle Dashboard is simple framework for creating a dashboard powered by [Slack](https://slack.com/).

I originally created the dashboard to display my bank balance on my [Raspberry Pi](https://www.raspberrypi.org/). 
Unfortunately the only way of knowing my balance without logging in to the bank's website was via a weekly SMS 
message they sent containing its balance, so using the automation app 
[Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) I was able to detect the SMS 
message, redirect it to a private Slack channel and have Doodle Dashboard extract the account balance and display it.


## Getting started

1. Install [Python 2.7](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/)

2. Clone Doodle Dashboard repository
```
$ git clone <PROJECT URL>
```

3. Install project dependencies   
```
$ cd doodle-dashboard
$ pip install -r requirements.txt
``` 

4. Create a configuration file
```
[Slack]
Token=<SLACK API TOKEN>
Channel=<NAME OF SLACK CHANNEL>
```

5. Start the dashboard
```
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