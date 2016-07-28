#!/usr/bin/env python
import argparse
import datetime
import eventbrite
import os
import logging
import report
import simplejson
import time

from flask import Flask, jsonify


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
    return simplejson.dumps(click_report(config))


def click_report(cfg):
    client = eventbrite.EventbriteClient(cfg['auth_token'])
    start = time.time()
    attendee_data = client.get_event_attendees(cfg['event_id'])
    # logging.debug(simplejson.dumps(attendee_data, indent=2))
    num_attendees = len(attendee_data)
    # people_who_were_checked_in = [x for x in attendee_data if x['checked_in'] is True]
    ticket_class_map = client.get_ticket_class_map(cfg['event_id'])
    checked_in_attendees = [x['checked_in'] for x in attendee_data if x['checked_in'] is True]
    num_checked_in = len(checked_in_attendees)
    adult_ticket_classes = [c['id'] for c in ticket_class_map if "adult" in c['name'].lower()]
    car_ticket_classes = [c['id'] for c in ticket_class_map if "car" in c['name'].lower()]
    adults_checked_in = [x['checked_in'] for x in attendee_data
                         if x['checked_in'] is True
                         and x['ticket_class_id'] in adult_ticket_classes]
    cars_checked_in = [x['checked_in'] for x in attendee_data
                       if x['checked_in'] is True
                       and x['ticket_class_id'] in car_ticket_classes]
    done = time.time()
    elapsed = done - start
    return {
        'timestamp': datetime.datetime.utcnow().isoformat("T") + "Z",
        'elapsed_seconds': elapsed,
        'num_attendees': num_attendees,
        'num_adults_checked_in': len(adults_checked_in),
        'num_cars_checked_in': len(cars_checked_in),
        # 'event': client.get_event(cfg['event_id']),
        # 'ticket_classes': client.get_ticket_classes(cfg['event_id']),
        # 'people_who_were_checked_in': people_who_were_checked_in,
        # 'attendees': attendee_data['attendees'],
        'num_checked_in': num_checked_in
    }

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
