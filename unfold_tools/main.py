from unfold_tools.sidebar import SIDEBAR

# تنظیمات اصلی unfold
UNFOLD = {
    "SITE_TITLE": "پنل مدیریت سایت",
    "SITE_HEADER": "سیستم مدیریت محتوا",
    "SITE_URL": "/",
    "SITE_ICON": None,  # مسیر آیکون سایت (اختیاری)

    # تنظیم اندازه صفحه
    "SIDEBAR_WIDTH": {
        "default": 280,  # عرض پیش‌فرض
        "collapsed": 64,  # عرض در حالت جمع شده
    },

    # رنگ‌های تم
    "COLORS": {
        "primary": {
            "50": "249 250 251",  # blueGray-50
            "100": "243 244 246",  # blueGray-100
            "200": "229 231 235",  # blueGray-200
            "300": "209 213 219",  # blueGray-300
            "400": "156 163 175",  # blueGray-400
            "500": "107 114 128",  # blueGray-500
            "600": "75 85 99",  # blueGray-600
            "700": "55 65 81",  # blueGray-700
            "800": "31 41 55",  # blueGray-800
            "900": "17 24 39",  # blueGray-900
        },
        "accent": {
            "500": "14 165 233",  # sky-500 (رنگ اصلی دکمه‌ها و لینک‌ها)
            "600": "2 132 199",  # sky-600 (رنگ هاور دکمه‌ها و لینک‌ها)
        }
    },

    # فونت‌ها - مناسب برای فارسی
    "FONTSHEET": "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css",
    "FONTS": {
        "default": "Vazirmatn, sans-serif",
        "monospace": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    },

    # تنظیمات RTL
    "RTL_SUPPORT": True,  # فعال کردن پشتیبانی RTL

    # تنظیمات منو
    "SIDEBAR": {
        "show_search": True,  # Enable search in sidebar
        "show_all_applications": False,
            "navigation": SIDEBAR
    },

    # بخش سفارشی‌سازی سربرگ

    # تنظیمات ENVIRONMENT برای نمایش محیط توسعه/تست/تولید
    "ENVIRONMENT": {
        "name": "محیط توسعه",
        "color": "red",  # رنگ نشانگر محیط
        "show": True,  # نمایش نشانگر محیط
    },

    # تنظیمات پیشرفته
    "USE_UNFOLD_FORM_CONTROLS": True,  # استفاده از کنترل‌های فرم unfold
    "USE_UNFOLD_SIDEBAR_ICONS": True,  # استفاده از آیکون‌های پیش‌فرض unfold
    "GRID_STYLE": "tailwind",  # سبک گرید (tailwind یا bootstrap)
}

