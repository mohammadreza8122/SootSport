from django.utils import translation


def rtl_processor(request):

    language = translation.get_language()
    is_rtl = language in ['fa', 'ar', 'he', 'ur']

    return {
        'is_rtl': is_rtl,
    }