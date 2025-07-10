"""
Base celery tasks
"""

from importlib import import_module

from celery import shared_task
import os
from django.utils.translation import gettext as _
import logging


@shared_task
def SendConfirm(phone, code):
    try:
        service = getattr(
            import_module(os.getenv("OTP_MODULE")), os.getenv("OTP_SERVICE")
        )()
        service.send_sms(
            phone, _("Sizning Tasdiqlash ko'dingiz: %(code)s") % {"code": code}
        )
        logging.info("Sms send: %s-%s" % (phone, code))
    except Exception as e:
        logging.error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )  # noqa
        raise Exception("Sms yuborishda xatolik yuzaga keldi")
