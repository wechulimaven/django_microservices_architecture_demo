import json
import logging

import requests
from django.core.serializers.json import DjangoJSONEncoder
from furl import furl

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Represents a base API client wrapper
    """

    def __init__(self, base_url):
        self._base_url = base_url
        self._request_session = requests.Session()
        self._request_session.headers.update(
            {
                "User-Agent": "makao/1.0",
                "Content-Type": "application/json",
            }
        )

    def _build_url(self, path):
        """
        Builds url from beam sdk base url
        :param path: path to endpoint
        :return: full endpoint URL
        """
        return furl(self._base_url).add(path=path)

    def _jsonify(self, dict_data):
        return json.dumps(dict_data, cls=DjangoJSONEncoder)

    def _get_json(self, response):
        try:
            return response.json()
        except ValueError:
            logger.exception("Could not get json body of response.")
            return {}

    def _get_json_response_data(self, response):
        """
        Extracts data from response if response has
        the valid status code provided else raises and exception
        :param response: response from service
        :param valid_status_code: valid status code to compare response status with
        :return: data (dict) from response json or raise exception for status >= 400
        """
        logger.debug("*****************Request*****************\n")
        logger.debug(f"request_url: {response.request.url}\n")
        logger.debug(f"request_body: {response.request.body}\n")
        logger.debug(f"request_headers: {response.request.headers}\n")
        logger.debug("*****************Response*****************\n")
        logger.debug(f"response_headers: {response.headers}\n")
        logger.debug(f"response_status_code: {response.status_code}\n")
        logger.debug(f"response_reason: {response.reason}\n")

        response_data = self._get_json(response=response)
        logger.debug(f"response_body: {response_data}\n")

        if response.ok:
            return response_data
        response.raise_for_status()

    def _fetch_json_response_data(self, response):
        logger.info("*****************Request*****************\n")
        logger.info(f"request_url: {response.request.url}\n")
        logger.info(f"request_body: {response.request.body}\n")
        logger.info(f"request_headers: {response.request.headers}\n")
        logger.info("*****************Response*****************\n")
        logger.info(f"response_headers: {response.headers}\n")
        logger.info(f"response_status_code: {response.status_code}\n")
        logger.info(f"response_reason: {response.reason}\n")

        response_data = self._get_json(response=response)
        logger.info(f"response_body: {response_data}\n")

        return response_data
