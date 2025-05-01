from django.utils.deprecation import MiddlewareMixin


class RTLMiddleware(MiddlewareMixin):
    """میان‌افزار برای پشتیبانی از راست‌چین سازی پنل ادمین"""

    def process_template_response(self, request, response):
        """پردازش پاسخ الگو و اضافه کردن متغیرهای مورد نیاز برای RTL"""
        if hasattr(response, 'context_data'):
            # افزودن متغیرهای RTL به context
            response.context_data['RTL_ENABLED'] = True
            response.context_data['LANGUAGE_BIDI'] = True

            # اضافه کردن کلاس‌های CSS به بدنه صفحه
            if 'body_class' in response.context_data:
                response.context_data['body_class'] += ' rtl'
            else:
                response.context_data['body_class'] = 'rtl'

        return response

    def process_response(self, request, response):
        """پردازش پاسخ HTTP و اضافه کردن هدرهای مربوط به RTL در صورت نیاز"""
        # اضافه کردن هدر جهت زبان برای مرورگرها
        response['Content-Language'] = 'fa'

        # اگر پاسخ HTML است، می‌توانیم هدرهای دیگری نیز اضافه کنیم
        if 'text/html' in response.get('Content-Type', ''):
            pass  # می‌توان هدرهای دیگری مرتبط با RTL اضافه کرد

        return response