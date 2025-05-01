def rtl_processor(request):
    """
    Context processor برای اضافه کردن متغیر is_rtl به تمام قالب‌ها

    از آنجا که فقط پشتیبانی از فارسی نیاز است، همیشه True برمی‌گرداند
    """

    # همیشه برای زبان فارسی راست‌چین خواهد بود
    return {
        'is_rtl': True,
    }