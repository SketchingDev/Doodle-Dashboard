import codecs
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}
with open(os.path.join(here, "doodledashboard", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__name__"],
    version=about["__version__"],
    description="Extensible dashboard designed to display data from multiple sources.",
    long_description=long_description,
    url="https://github.com/SketchingDev/Doodle-Dashboard",
    license="MIT",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "requests",
        "slackclient",
        "feedparser",
        "pyyaml",
        "click",
        "doodle-dashboard-display-console>=0.0.16"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "doodledashboard=doodledashboard.cli:cli"
        ],
        "doodledashboard.custom.filters": [
            "contains-text=doodledashboard.filters.contains_text:ContainsTextFilter",
            "matches-regex=doodledashboard.filters.matches_regex:MatchesRegexFilter"
        ],
        "doodledashboard.custom.datafeeds": [
            "datetime=doodledashboard.datafeeds.datetime:DateTimeFeed",
            "rss=doodledashboard.datafeeds.rss:RssFeed",
            "slack=doodledashboard.datafeeds.slack:SlackFeed",
            "text=doodledashboard.datafeeds.text:TextFeed"
        ],
        "doodledashboard.custom.notifications": [
            "text=doodledashboard.notifications:TextNotification",
            "image=doodledashboard.notifications:ImageNotification",
            "image-with-text=doodledashboard.notifications:ImageWithTextNotification",
            "colour=doodledashboard.notifications:ColourNotification"
        ],
        "doodledashboard.custom.notification.updaters": [
            "image=doodledashboard.updaters.image.image:ImageNotificationUpdater",
            "text=doodledashboard.updaters.text.text:TextNotificationUpdater"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.4"
    ],
    python_requires=">=3.4"
)
