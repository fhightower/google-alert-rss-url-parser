#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to parse URLs from Google alert rss feed."""

import argparse
import configparser
import re
import sys

import feedparser
from threatconnect import ThreatConnect

indicator_metadata_config = {
    'confidence_rating': 50,
    'threat_rating': 2.5,
    'description': "",
    # if owner is None, it will use the default owner from the API config
    'owner': None,
    'security_label': "TLP White",
    'tags': ["Google Alert"]
}


def init_parser():
    """Initialize the argument parser."""
    parser = argparse.ArgumentParser(description="Parse URL from " +
                                     "Google Alerts RSS feed.")
    parser.add_argument(dest="google_alert_rss_url", type=str,
                        help="URL of Google alert rss feed")

    return parser.parse_args()


def init_threat_connect():
    """."""
    config = configparser.RawConfigParser()
    config.read('tc.conf.example')

    try:
        api_access_id = config.get('threatconnect', 'api_access_id')
        api_secret_key = config.get('threatconnect', 'api_secret_key')
        api_default_org = config.get('threatconnect', 'api_default_org')
        api_base_url = config.get('threatconnect', 'api_base_url')
    except configparser.NoOptionError:
        print('Could not read configuration file.')
        sys.exit(1)
    else:
        tc = ThreatConnect(api_access_id, api_secret_key, api_default_org,
                           api_base_url)
        return tc


def clean_google_url(google_search_string):
    """Parse the URL from a google URL (with all of the Google tracking)."""
    url = re.match(".*?&url=(http.*?)&ct=.*", google_search_string)

    return url.group(1)


def create_indicator(tc, url_indicator):
    """Create the URL indicator in ThreatConnect."""
    indicators = tc.indicators()

    if indicator_metadata_config['owner'] is None:
        owner = api_default_org
    else:
        owner = indicator_metadata_config['owner']

    indicator = indicators.add(url_indicator, owner)

    indicator.set_confidence(indicator_metadata_config['confidence_rating'])
    indicator.set_rating(indicator_metadata_config['threat_rating'])
    indicator.add_attribute('Description',
                            indicator_metadata_config['description'])

    for tag in indicator_metadata_config['tags']:
        indicator.add_tag(tag)

    indicator.set_security_label(indicator_metadata_config['security_label'])

    try:
        indicator.commit()
    except RuntimeError as e:
        print('Error: {0}'.format(e))


def main():
    """Get URLs from the Google alert RSS feed."""
    args = init_parser()
    tc = init_threat_connect()

    feed = feedparser.parse(args.google_alert_rss_url)

    for entry in feed['entries']:
        clean_url = clean_google_url(entry.link)
        create_indicator(tc, clean_url)


if __name__ == '__main__':
    main()
