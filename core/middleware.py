class RTLMiddleware:
    """
    میان‌افزار برای اعمال RTL به تمام صفحات

    این میان‌افزار همیشه متغیر is_rtl را به True تنظیم می‌کند
    چون ما فقط نسخه فارسی و راست‌چین نیاز داریم
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # همیشه RTL را فعال می‌کند
        request.is_rtl = True

        response = self.get_response(request)
        return response