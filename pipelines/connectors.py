import logging
import requests as req
from keys import API_KEY

class congressDotGovClient():

    def __init__(self, url: str=None, logger: object=None):
        self.logger = logger or logging.getLogger(__name__)
        self._url = url
        self._api_key = API_KEY
        self.params = {'api_key': self._api_key}
    
    def get(self, target_url=None):
        """
        Method for fetching data from the API and returning it as JSON.

        If you want the full request object, try call() instead.
        """
        object_raw = self.call(target_url) if target_url else self.call(self._url)
        object_json = object_raw.json()
        return object_json
    
    def call(self, url):
        """
        Makes an API call and returns the full request object.

        Raises logger warning if a non-200 status is returned
        """
        self.logger.info('Making call with %s' % url)
        req_obj = req.get(url, params=self.params)
        self.status_code = req_obj.status_code
        self.logger.info('Call made, returning response')
        if req_obj.status_code != 200:
            self.logger.warning('Call returned non-200'
                                ' status of %s' % req_obj.status_code)
        return req_obj

    def paginate(self):
        """
        Generator that makes the initial call to a URL then paginates through
        the rest of the results.

        Returns the entire response, one page at a time then clears the params.
        """
        target_url = self._url
        while target_url:
            self.logger.info('Getting data')
            data = self.get(target_url)
            yield data
            if 'next' in data['pagination'].keys():
                self.logger.info('Heading to next page')
                target_url = data['pagination']['next']
            else:
                self.logger.debug('No more target_url, finishing pagination')
                target_url = None