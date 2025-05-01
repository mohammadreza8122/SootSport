from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Utility function to generate admin page URL
def admin_page(app, model):
    try:
        return reverse_lazy(f"admin:{app}_{model}_changelist")
    except (LookupError, TypeError) as e:
        raise ValueError(f"App '{app}' or model '{model}' not found. Error: {str(e)}")


# Utility function to create sidebar items
def create_sidebar_item(app, model, title, icon):
    return {
        "title": _(title),
        "icon": icon,
        "link": admin_page(app, model),
    }

# Utility function to create custom URL sidebar items
def create_custom_sidebar_item(title, icon, url):
    return {
        "title": _(title),
        "icon": icon,
        "link": reverse_lazy(url),
    }


# Icon mapping for consistency and ease of use
ICON_MAP = {
    'dashboard': 'dashboard',
    'group': 'groups',
    'user': 'person',
    'province': 'public',
    'city': 'location_city',
    'address': 'pin_drop',
    'brand': 'brand_family',
    'category': 'category',
    'tag': 'tag',
    'sport_facility': 'stadium',
    'discount': 'local_offer',
    'timeslot': 'schedule',
    'reservation': 'bookmark_added',
    'website': 'dns',
    'site': 'dns',
    'organization': 'domain',
    'accessory': 'media_output',
    'mobile': 'phone_iphone',
    'tablet': 'tablet_mac',
    'creator': 'interpreter_mode',
    'video': 'videocam',
}


# Define the dashboard section with correct structure
dashboard_section = {
    "title": _("داشبورد"),
    "icon": ICON_MAP['dashboard'],
    "collapsible": False,
    "items": [
        {
            "title": _("نمای کلی"),
            "icon": ICON_MAP['dashboard'],
            "link": reverse_lazy('admin_dashboard'),
        }
    ]
}

# Define the list of sidebar items dynamically
user_list = [
    create_sidebar_item('auth', 'group', 'گروه‌ها', ICON_MAP['group']),
    create_sidebar_item('user', 'user', 'کاربران', ICON_MAP['user']),
]

address_list = [
    create_sidebar_item('address', 'province', 'استان‌ها', ICON_MAP['province']),
    create_sidebar_item('address', 'city', 'شهرها', ICON_MAP['city']),
    create_sidebar_item('address', 'address', 'آدرس‌ها', ICON_MAP['address']),
]

provider_list = [
    create_sidebar_item('provider', 'category', 'دسته‌بندی‌ها', ICON_MAP['category']),
    create_sidebar_item('provider', 'tag', 'تگ‌ها', ICON_MAP['tag']),
    create_sidebar_item('provider', 'sportfacility', 'سالن‌های ورزشی', ICON_MAP['sport_facility']),
    create_sidebar_item('provider', 'discount', 'تخفیف‌ها', ICON_MAP['discount']),
    create_sidebar_item('provider', 'timeslot', 'سانس‌ها', ICON_MAP['timeslot']),
    create_sidebar_item('provider', 'reservation', 'رزروها', ICON_MAP['reservation']),
]

# Utility function to create sidebar sections
def create_sidebar_section(title, icon, items):
    return {
        "title": _(title),
        "collapsible": True,
        "icon": icon,
        "items": items,
    }


# Sidebar structure
SIDEBAR = [
    create_sidebar_section(_("کاربران و دسترسی"), "manage_accounts", user_list),
    create_sidebar_section(_("آدرس‌ها"), "location_on", address_list),
    create_sidebar_section(_("مدیریت سالن‌ها"), "storefront", provider_list),
#     create_sidebar_section(_("Taxonomy"), "category", taxonomy_list),
#     create_sidebar_section(_("Video"), "videocam", video_list),
]
#
#



# "badge": "sample_app.badge_callback",
#
# def badge_callback(request):
#     return 3


# "permission": lambda request: request.user.is_superuser,
# "permission": "sample_app.permission_callback",
# def permission_callback(request):
#     return request.user.has_perm("sample_app.change_model")