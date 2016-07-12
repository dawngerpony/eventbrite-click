#!/usr/bin/env python
import argparse
import eventbrite
import os
import logging
import report


def load_config():
    logging.debug("load_config()")
    return {
        "auth_token": os.getenv("EVENTBRITE_PERSONAL_OAUTH_TOKEN"),
        "base_url":   "https://www.eventbriteapi.com/v3"
    }


def run():
    logging.debug("run()")
    config = load_config()
    args = parse_args()
    client = eventbrite.EventbriteClient(config['auth_token'])
    report.print_click_report(client, args.eventId)
    # print simplejson.dumps(client.get_users_me())
    # print simplejson.dumps(client.get_users_me_owned_events())
    # print simplejson.dumps(client.get_event_attendees(args.eventId))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("eventId", help="event ID")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("eventbrite-click")
    run()
