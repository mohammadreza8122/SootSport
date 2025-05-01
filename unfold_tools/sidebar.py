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


# Icon mapping for consistency and ease of use
ICON_MAP = {
    'group': 'groups',
    'user': 'person',
    'brand': 'brand_family',
    'category': 'nest_gale_wifi',
    'website': 'dns',
    'tag': 'tag',
    'site': 'dns',
    'organization': 'domain',
    'accessory': 'media_output',
    'mobile': 'phone_iphone',
    'tablet': 'tablet_mac',
    'creator': 'interpreter_mode',
    'video': 'videocam',
}


# Define the list of sidebar items dynamically
user_list = [
    create_sidebar_item('auth', 'group', 'گروه', ICON_MAP['group']),
    create_sidebar_item('user', 'user', 'کاربران', ICON_MAP['user']),
]

address_list = [
    create_sidebar_item('address', 'province', 'استان ها', ICON_MAP['group']),
    create_sidebar_item('address', 'city', 'شهر ها', ICON_MAP['user']),
]

provider_list = [
    # create_sidebar_item('taxonomy', 'brand', 'brand', ICON_MAP['brand']),
    # create_sidebar_item('taxonomy', 'category', 'category', ICON_MAP['category']),
    # create_sidebar_item('taxonomy', 'tag', 'tag', ICON_MAP['tag']),
    # create_sidebar_item('website', 'website', 'website', ICON_MAP['website']),
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
    create_sidebar_section(_("کاربران"), "account_circle", user_list),
    create_sidebar_section(_("استان‌ها و شهرها"), "domain", address_list),
    create_sidebar_section(_("سالن ها"), "shopping_cart", provider_list),
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