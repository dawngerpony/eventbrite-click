#!/usr/bin/env python
import argparse
import eventbrite
import os
import logging
import report
from flask import Flask


ENVVAR_EVENTBRITE_PERSONAL_OAUTH_TOKEN = "EVENTBRITE_PERSONAL_OAUTH_TOKEN"
ENVVAR_EVENTBRITE_EVENT_ID = "EVENTBRITE_EVENT_ID"
ENVVAR_HEROKU_PORT = "PORT"

app = Flask(__name__)


def load_config():
    logging.debug("load_config()")
    return {
        'auth_token': os.getenv(ENVVAR_EVENTBRITE_PERSONAL_OAUTH_TOKEN),
        'event_id':   os.getenv(ENVVAR_EVENTBRITE_EVENT_ID),
        'port':       os.getenv(ENVVAR_HEROKU_PORT, '5000'),
        'base_url':   'https://www.eventbriteapi.com/v3'
    }


def run():
    logging.debug("run()")
    config = load_config()
    # args = parse_args()
    client = eventbrite.EventbriteClient(config['auth_token'])
    # logging.debug(config)
    app.run(port=config['port'])
    # report.print_click_report(client, args.eventId)
    # print simplejson.dumps(client.get_users_me())
    # print simplejson.dumps(client.get_users_me_owned_events())
    # print simplejson.dumps(client.get_event_attendees(args.eventId))


@app.route("/")
def hello():
    return "Hello World!"


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
