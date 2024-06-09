import logging
from django.conf import settings
from requests import HTTPError

from services.api_client import BaseClient

logger = logging.getLogger("__name__")


class ServiceError(Exception):
    def __init__(self, reason):
        super().__init__(reason)


class PostService(BaseClient):
    def __init__(
        self,
    ):
        super().__init__(settings.POST_SERVICE_BASE_URL)
        self.api_key = settings.POST_SERVICE_SECRET_KEY
        self._request_session.headers.update({"Authorization": f"Token {self.api_key}"})

    def _is_successful_response(self, response_data):
        response_status = response_data.get("status")
        if response_status is True:
            return True
        raise HTTPError("User service request failed.")

    def get_feeds(self):
        url = self._build_url(f"/post/all/")
        response = self._request_session.get(url)
        try:
            response_data = self._get_json_response_data(response)
            if self._is_successful_response(response_data=response_data):
                logger.info(response_data.get("data"))
                return True, response_data.get("data")

        except (HTTPError, Exception) as e:
            logger.error("Encountered an error %s" % str(e))

            return False, self._get_json(response=response).get("data", str(e))

    def get_feed_detail(self, id):
        url = self._build_url(f"/post/detail/{id}/")
        response = self._request_session.get(url)
        try:
            response_data = self._get_json_response_data(response)
            if self._is_successful_response(response_data=response_data):
                logger.info(response_data.get("data"))
                return True, response_data.get("data")

        except (HTTPError, Exception) as e:
            logger.error("Encountered an error %s" % str(e))

            return False, self._get_json(response=response).get("data", str(e))

    def add_feed(self, user_id, title, body, image:None):
        url = self._build_url(f"/post/create/")
        json_data = self._jsonify(
            {
                "user_id": user_id,
                "title": title,
                "body": body,
                "image": image,
            }
        )
        response = self._request_session.post(url, data=json_data)
        try:
            response_data = self._get_json_response_data(response)
            if self._is_successful_response(response_data=response_data):
                logger.info(response_data.get("data"))
                return True, response_data.get("data")
        except (HTTPError, Exception) as e:
            logger.error("Encountered an error %s" % str(e))
            return False, self._get_json(response=response).get("data", str(e))
