# Eventbrite API client
import http
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

    def get_event_attendees(self, event_id):
        return self._get("events/{}/attendees".format(event_id))

    def _get(self, path):
        url = "{}/{}?token={}".format(self.base_url, path, self.token)
        return self.http_client.get(url)

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
