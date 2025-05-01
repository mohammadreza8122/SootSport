from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold_tools.sidebar import SIDEBAR


def set_direction(request):
    """همیشه جهت RTL برای فارسی"""
    return 'rtl'


UNFOLD = {
    # عنوان سایت و هدر
    "SITE_TITLE": "مدیریت سوت اسپورت",
    "SITE_HEADER": "پنل مدیریت سوت اسپورت",
    "SITE_URL": "/",

    # آیکون و لوگو
    "SITE_ICON": lambda request: static("cropped-icon-2-192x192.webp"),
    "SITE_LOGO": lambda request: static("cropped-icon-2-192x192.webp"),

    # گزینه‌های نمایش
    "SHOW_HISTORY": True,  # نمایش دکمه "تاریخچه"
    "SHOW_VIEW_ON_SITE": True,  # نمایش دکمه "مشاهده در سایت"

    "ENVIRONMENT": "unfold_tools.utils.environment_callback",

    # تنظیم جهت RTL
    "DIRECTION": set_direction,  # همیشه RTL برای فارسی

    # تنظیمات ورود
    "LOGIN": {
        "image": lambda request: static("login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),  # هدایت به داشبورد پس از ورود
    },

    # استایل‌ها و اسکریپت‌های سفارشی
    "STYLES": [
        lambda request: static("custom.css"),  # فایل CSS سفارشی
    ],
    "SCRIPTS": [
        lambda request: static("custom.js"),  # فایل JavaScript سفارشی
    ],

    # تنظیمات ظاهری
    "BORDER_RADIUS": "20px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },

    # تنظیمات فونت
    "FONTSHEET": "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css",
    "FONTS": {
        "default": "Vazirmatn, sans-serif",
        "monospace": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    },

    # نوار کناری
    "SIDEBAR": {
        "show_search": True,  # فعال کردن جستجو در نوار کناری
        "show_all_applications": False,
        "navigation": SIDEBAR
    },

    # فعال کردن RTL
    "RTL_SUPPORT": True,
}