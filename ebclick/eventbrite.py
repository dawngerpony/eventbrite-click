# Eventbrite API client
import http
import http_multi
import logging
import pickle
import time


def write_responses_data(data):
    """ Write a list of HTTP response data to disk using pickle,
        for the purpose of automated testing and offline development.
    """
    filename = 'data_{}.requests.models.Response.p'.format(time.time())
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


class EventbriteClient:

    base_url = "https://www.eventbriteapi.com/v3"
    token = None
    cache_filename = "/tmp/eventbrite.cache"
    cache = None
    http_client = None
    cache_to_disk = False

    def __init__(self, token, base_url=None, cache_to_disk=False):
        logging.debug("EventbriteClient __init__")
        if base_url:
            self.base_url = base_url
        self.token = token
        self.cache_to_disk = cache_to_disk
        # self.cache = shelve.open(self.cache_filename)
        self.http_client = http.CachingHttpClient()

    def get_users_me(self):
        return self._get("users/me/")

    def get_users_me_owned_events(self):
        return self._get("users/me/owned_events")

    def get_event(self, event_id):
        return self._get("events/{}".format(event_id))

    def get_ticket_classes(self, event_id):
        return self._get("events/{}/ticket_classes/".format(event_id))

    def get_ticket_class_map(self, event_id):
        ticket_classes = self.get_ticket_classes(event_id)
        m = {}
        classes = [{'id': t['id'], 'name': t['name']} for t in ticket_classes['ticket_classes']]
        return classes

    def get_event_attendees(self, event_id):
        attendees_path_prefix = "events/{}/attendees/".format(event_id)
        ticket_class_map = self.get_ticket_class_map(event_id)
        logging.debug(ticket_class_map)
        page1 = self._get(attendees_path_prefix, page=1)
        num_pages = page1['pagination']['page_count']
        # num_pages = 2 # for dev
        # pages = [page1]
        urls = self._build_urls(attendees_path_prefix, start_page=2, end_page=num_pages)
        responses = http_multi.get_multi(urls)
        if self.cache_to_disk is True:
            write_responses_data(responses)
        # attendee_data = AttendeeData(responses)
        # logging.debug(responses)
        attendees = []
        # for p in pages:
        #     attendees += p['attendees']
        # logging.debug('pages={}'.format(len(pages)))
        return attendees

    def _build_urls(self, path, start_page=1, end_page=1):
        urls = []
        logging.debug('start_page={} end_page={}'.format(start_page, end_page))
        for i in range(start_page, end_page):
            url = "{}/{}?token={}&page={}".format(self.base_url, path, self.token, i)
            urls.append(url)
        logging.debug('urls={}'.format(len(urls)))
        return urls

    def _get(self, path, page=1):
        url = "{}/{}?token={}&page={}".format(self.base_url, path, self.token, page)
        logging.debug(url)
        return self.http_client.get(url, use_cache=False)

    # def _get(self, path, use_cache=True):
    #     """ Get object from the API, using the cache if possible.
    #     """
    #     key = self._cache_key(path)
    #     url = "{}/{}?token={}".format(self.base_url, path, self.token)
    #     if use_cache is True:
    #         logging.debug("Using cached data for path=\"{}\"".format(path))
    #         logging.debug("Cache keys: {}".format(self.cache.keys()))
    #         if key in self.cache:
    #             return self.cache[key]
    #         else:
    #             return self._cache_store(path, requests.get(url).json())
    #     else:
    #         return requests.get(url).json()

    def _cache_key(self, suffix):
        return "{}_{}".format(self.token, suffix)

    def _cache_store(self, suffix, data):
        """ Store data in the cache.
        """
        self.cache[self._cache_key(suffix)] = data
        return data


class AttendeeData:

    pages = []
    attendees = []
    responses = []
    timestamp = None

    def __init__(self, responses):
        self.responses = responses
        # for r in responses:
        #     print(r)

    def total_checked_in(self):
        """ Return a total of the attendees that have been checked in. Includes all ticket types.
        """
        # TODO Finish this.
        return 0

    def total_human_attendees(self):
        """ Return the total number of attendees, including all ticket types.
        """
        # TODO Finish this.
        return 0

    def percentage_humans_checked_in(self):
        """ Return a tuple of:
                - 1: the number of humans attending the event
                - 2: the number of humans that have been checked in to the event
                - 3: for convenience, the percentage of humans out of the total
        """
        # TODO Finish this.
        return (0, 0, 0)
