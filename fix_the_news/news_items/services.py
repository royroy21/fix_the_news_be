import logging

import requests
from requests import exceptions as requests_exceptions


logger = logging.getLogger(__name__)


class NewsItemURLService:

    PREPEND_HTTP = 'http://'
    PREPEND_HTTPS = 'https://'

    def parse_and_validate(self, url):
        """ Returns parsed url and validation error if error exists """
        https_url = self.parse(url)
        error = self.validate(https_url)
        if error:
            http_url = self.parse(url, force_http=True)
            error = self.validate(http_url)
            if error:
                return url, error
            return http_url, None
        return https_url, None

    def parse(self, url, force_http=False):
        if url.startswith(self.PREPEND_HTTP) \
                or url.startswith(self.PREPEND_HTTPS):
            return url

        if force_http:
            return f"{self.PREPEND_HTTP}{url}"

        return f"{self.PREPEND_HTTPS}{url}"

    def validate(self, url):
        """ Returns an error if URL is not valid otherwise None """
        try:
            response = requests.get(url)
        except (
            requests_exceptions.ConnectionError,
            requests_exceptions.ConnectTimeout,
            requests_exceptions.SSLError,
        ) as error:
            logger.error(
                'Error validating URL:%s error:%s',
                url,
                error,
            )
            return error

        if not response.ok:
            logger.error(
                'Error validating URL:%s status_code:%s response:%s',
                url,
                response.status_code,
                response.text,
            )
            return 'Unexpected error'

        return None
