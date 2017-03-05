# Google Alert RSS URL Parser

Using [Google Alerts](https://www.google.com/alerts), it is possible to collect interesting content that matches a specified search term into an RSS feed (or get an email about it).

This script is designed to parse the URL out of every entry in the RSS feed. The master branch contains a simple version of the script and other branches provide more specific functionality like the ability to create each URL found from an alert in [ThreatConnect](https://app.threatconnect.com).

## Usage

To use this script:

1. Setup a [Google Alert](https://www.google.com/alerts) that interests you. Be sure to set the alert to deliver to an RSS feed rather than via email.
2. Run the following command to clone this repository: 
  `git clone https://gitlab.com/exoneris/google-alert-rss-url-parser.git`
3. On the [Google Alerts](https://www.google.com/alerts) page, copy the link to the RSS feed for the alert which you would like to monitor.
4. Setup a [crontab](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/) or similar system that will run the script on a regular basis. An example crontab entry that would run the script every 30 minutes would look like:

    `*/30 * * * * python3 /PATH/TO/SCRIPT/google-alert-rss-url-parser.py <GOOGLE_ALERT_RSS_FEED_URL_HERE>`

Note that the script expects the URL to the Google alert RSS feed to be passed in as an argument. For example, this may look something like:

    `python3 google-alert-rss-url-parser.py https://www.google.com/alerts/feeds/12345/67890`