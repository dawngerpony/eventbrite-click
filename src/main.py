#!/usr/bin/env python
import argparse
import eventbrite
import os
import logging
import report
import simplejson
from flask import Flask


ENVVAR_EVENTBRITE_PERSONAL_OAUTH_TOKEN = "EVENTBRITE_PERSONAL_OAUTH_TOKEN"
ENVVAR_EVENTBRITE_EVENT_ID = "EVENTBRITE_EVENT_ID"
ENVVAR_HEROKU_PORT = "PORT"

app = Flask(__name__)


def load_config():
    logging.debug("load_config()")
    # in_heroku = (os.getenv(ENVVAR_HEROKU_PORT, '') != '')
    # logging.debug("in_heroku: {}".format(in_heroku))
    c = {
        'auth_token': os.getenv(ENVVAR_EVENTBRITE_PERSONAL_OAUTH_TOKEN),
        'event_id':   os.getenv(ENVVAR_EVENTBRITE_EVENT_ID),
        'port':       int(os.getenv(ENVVAR_HEROKU_PORT, '5000')),
        'base_url':   'https://www.eventbriteapi.com/v3'
    }
    return c


def run():
    logging.debug("run()")
    config = load_config()
    # args = parse_args()

    # logging.debug(config)
    app.run(host='0.0.0.0', port=config['port'])
    # report.print_click_report(client, args.eventId)
    # print simplejson.dumps(client.get_users_me())
    # print simplejson.dumps(client.get_users_me_owned_events())
    # print simplejson.dumps(client.get_event_attendees(args.eventId))


@app.route("/")
def hello():
    logging.debug("hello()")
    config = load_config()
    # client = eventbrite.EventbriteClient('test')
    # logging.debug("OAuth token: {}".format(config['auth_token']))
    client = eventbrite.EventbriteClient(config['auth_token'])
    return simplejson.dumps(client.get_users_me())


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
