from django.conf import settings
import jdatetime

def rtl_processor(request):
    return {
        # 'LANGUAGE_BIDI': True, # حذف شد - توسط Unfold مدیریت می‌شود
        # 'RTL_ENABLED': True, # حذف شد - توسط Unfold مدیریت می‌شود
        'LANGUAGE_CODE': settings.LANGUAGE_CODE, # این می‌تواند مفید باشد
        'JALALI_NOW': jdatetime.datetime.now().strftime('%Y/%m/%d'),
        'JALALI_YEAR': jdatetime.datetime.now().year,
        'JALALI_MONTH': jdatetime.datetime.now().month,
        'JALALI_DAY': jdatetime.datetime.now().day,
        'JALALI_MONTH_NAME': jdatetime.date.j_months_fa[jdatetime.datetime.now().month-1],
    }