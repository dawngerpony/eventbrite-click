# Eventbrite API client
import http
import http_multi
import logging


class EventbriteClient():

    base_url = "https://www.eventbriteapi.com/v3"
    token = None
    cache_filename = "/tmp/eventbrite.cache"
    cache = None
    http_client = None

    def __init__(self, token, base_url=None):
        logging.debug("EventbriteClient __init__")
        if base_url:
            self.base_url = base_url
        self.token = token
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
        ticket_class_map = self.get_ticket_class_map(event_id)
        logging.debug(ticket_class_map)
        page1 = self._get("events/{}/attendees".format(event_id, 1))
        num_pages = page1['pagination']['page_count']
        # num_pages = 10 # for dev
        pages = [page1]
        path = "events/{}/attendees".format(event_id)
        urls = self._build_urls(path, 2, num_pages)
        # for i in range(2, num_pages):
        #     data = self._get("events/{}/attendees".format(event_id))
        #     pages.append(data)
        # logging.debug("len(pages)={}".format(len(pages)))
        responses = http_multi.get_multi(urls)
        logging.debug(responses)
        attendees = []
        for p in pages:
            attendees += p['attendees']
        return attendees

    def _build_urls(self, path, start_page=1, end_page=1):
        urls = []
        for i in range(start_page, end_page):
            url = "{}/{}?token={}&page={}".format(self.base_url, path, self.token, i)
            urls.append(url)
        return urls


    def _get(self, path, page=1, use_multi=False):
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
