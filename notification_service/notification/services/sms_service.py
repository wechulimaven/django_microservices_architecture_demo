import logging
from django.conf import settings

import africastalking

logger = logging.getLogger('__name__')

class SMSClient:
    def __init__(self, recepient, message):
        self.username = settings.SMS_USERNAME
        self.api_key = settings.SMS_API_KEY
        self.recepient = recepient
        self.message = message

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self):
        try:
            logger.info(f"SMS PARAMS {self.message}, {self.recepient}")
            # Thats it, hit send and we'll take care of the rest.
            recepients = self.recepient if isinstance(self.recepient, list) else [self.recepient]
            response = self.sms.send(self.message, recepients)
            logger.info(f"SMS RESPONSE {response}")

        except Exception as e:
            logger.error('Encountered an error while sending: %s' % str(e))
