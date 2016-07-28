# Caching HTTP client using the requests library.
import logging
import requests
import shelve


class CachingHttpClient:

    cache_filename = "/tmp/eventbrite.cache"
    cache = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        # self.token = token
        self.cache = shelve.open(self.cache_filename)

    def get(self, url, use_cache=True):
        """ Get object from the API, using the cache if possible.
        """
        cache_key = url
        if use_cache is True:
            logging.debug("Using cached data for url=\"{}\"".format(url))
            logging.debug("Cache keys: {}".format(self.cache.keys()))
            if url in self.cache:
                return self.cache[cache_key]
            else:
                return self._cache_store(cache_key, requests.get(url).json())
        else:
            logging.debug("Retrieving url='{}'".format(url))
            return requests.get(url).json()

    def _cache_store(self, key, data):
        """ Store data in the cache.
        """
        self.cache[key] = data
        return data
