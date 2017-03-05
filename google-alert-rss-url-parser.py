#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to parse URLs from Google alert rss feed."""

import argparse
import re

import feedparser


def init_parser():
    """Initialize the argument parser."""
    parser = argparse.ArgumentParser(description="Parse URL from " +
                                     "Google Alerts RSS feed.")
    parser.add_argument(dest="google_alert_rss_url", type=str,
                        help="URL of Google alert rss feed")

    return parser.parse_args()


def clean_google_url(google_search_string):
    """Parse the URL from a google URL (with all of the Google tracking)."""
    url = re.match(".*?&url=(http.*?)&ct=.*", google_search_string)

    return url.group(1)


def main():
    """Get URLs from the Google alert RSS feed."""
    args = init_parser()

    feed = feedparser.parse(args.google_alert_rss_url)

    for entry in feed['entries']:
        clean_url = clean_google_url(entry.link)
        print(clean_url)


if __name__ == '__main__':
    main()
