# -*- coding: utf-8 -*-
from django.utils import timezone
import jdatetime
from django import forms
from datetime import datetime


def gregorian_to_jalali(date_obj):
    """تبدیل تاریخ میلادی به شمسی"""
    if date_obj is None:
        return None

    if isinstance(date_obj, datetime):
        return jdatetime.datetime.fromgregorian(datetime=date_obj)
    else:
        return jdatetime.date.fromgregorian(date=date_obj)


def jalali_to_gregorian(jdate):
    """تبدیل تاریخ شمسی به میلادی"""
    if jdate is None:
        return None

    if isinstance(jdate, jdatetime.datetime):
        return jdate.togregorian()
    else:
        return jdate.togregorian()


class JDateField(forms.CharField):
    """فیلد فرم برای تاریخ جلالی"""

    def __init__(self, *args, **kwargs):
        super(JDateField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """تبدیل رشته به تاریخ جلالی"""
        if value in self.empty_values:
            return None

        try:
            jdate = jdatetime.datetime.strptime(value, '%Y/%m/%d').date()
            return jalali_to_gregorian(jdate)
        except (ValueError, TypeError):
            raise forms.ValidationError("فرمت تاریخ باید به صورت YYYY/MM/DD باشد.")

    def prepare_value(self, value):
        """آماده‌سازی مقدار برای نمایش در فرم"""
        if value is None:
            return ''

        if isinstance(value, str):
            return value

        try:
            jdate = gregorian_to_jalali(value)
            return jdate.strftime('%Y/%m/%d')
        except (ValueError, TypeError, AttributeError):
            return value


class JDateTimeField(forms.CharField):
    """فیلد فرم برای تاریخ و زمان جلالی"""

    def __init__(self, *args, **kwargs):
        super(JDateTimeField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """تبدیل رشته به تاریخ و زمان جلالی"""
        if value in self.empty_values:
            return None

        try:
            jdt = jdatetime.datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
            return jalali_to_gregorian(jdt)
        except (ValueError, TypeError):
            raise forms.ValidationError("فرمت تاریخ و زمان باید به صورت YYYY/MM/DD HH:MM:SS باشد.")

    def prepare_value(self, value):
        """آماده‌سازی مقدار برای نمایش در فرم"""
        if value is None:
            return ''

        if isinstance(value, str):
            return value

        try:
            jdt = gregorian_to_jalali(value)
            return jdt.strftime('%Y/%m/%d %H:%M:%S')
        except (ValueError, TypeError, AttributeError):
            return value


def get_jalali_now():
    """دریافت تاریخ و زمان فعلی به صورت شمسی"""
    return gregorian_to_jalali(timezone.now())