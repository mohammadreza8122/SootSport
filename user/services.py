# services.py
import random
from datetime import timedelta
from django.utils import timezone
from .models import OTP


def generate_otp(phone_number):
    OTP.objects.filter(phone_number=phone_number).delete()

    code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

    expires_at = timezone.now() + timedelta(minutes=5)

    otp = OTP.objects.create(
        phone_number=phone_number,
        code=code,
        expires_at=expires_at
    )

    return code


def verify_otp(phone_number, code):
    try:
        otp = OTP.objects.get(phone_number=phone_number, code=code)
        if otp.is_valid():
            # حذف کد پس از استفاده
            otp.delete()
            return True
        # کد منقضی شده است
        otp.delete()
        return False
    except OTP.DoesNotExist:
        return False