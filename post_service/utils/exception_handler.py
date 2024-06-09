import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError

from rest_framework.exceptions import APIException

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)



def custom_error_response(errors, message):
    return {
        "status": False,
        "message": message if message is not None else _("An exception occured"),
        **errors,
    }

def custom_exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    # ...
    'EXCEPTION_HANDLER': 'mtp.apps.common.drf.exception_handler',
    # ...
    For the parameters, see ``exception_handler``
    """
    if (
        isinstance(exc, DjangoValidationError)
        or isinstance(exc, IntegrityError)
        or isinstance(exc, ObjectDoesNotExist)
    ):
        if hasattr(exc, "message_dict"):
            logger.info("HERE===>")
            exc = DRFValidationError(
                detail=custom_error_response({"errors": exc.message_dict})
            )
        elif hasattr(exc, "message"):
            exc = DRFValidationError(
                detail=custom_error_response({"errors": [exc.message]})
            )
        elif hasattr(exc, "messages"):
            exc = DRFValidationError(
                detail=custom_error_response({"errors": exc.messages}, exc.messages)
            )
        else:
            exc = DRFValidationError(
                detail=custom_error_response({"errors": [str(exc)]}, exc)
            )
    elif type(exc) == Exception:
        logger.error(f"EXCEPTION <=======> {exc}")
        exc = APIException(
            detail=custom_error_response(exc.message, {"errors": exc.message})
        )

    return drf_exception_handler(exc, context)