import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.admin.models import LogEntry
from django.db import connection
from django import get_version
import sys

User = get_user_model()

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # آمار کاربران
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        user_percentage = int((active_users / total_users) * 100) if total_users > 0 else 0
        
        # به دست آوردن مدل‌های محتوا (این بخش باید متناسب با پروژه شما تغییر کند)
        # این یک مثال کلی است
        try:
            from django.apps import apps
            content_models = []
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    # فقط مدل‌هایی که مربوط به محتوا هستند را اضافه کنید
                    # (این منطق باید متناسب با پروژه شما سفارشی شود)
                    if hasattr(model, '_meta') and not model._meta.model_name in ['user', 'group', 'permission', 'logentry']:
                        content_models.append(model)
            
            total_content = sum(model.objects.count() for model in content_models)
            # فرض می‌کنیم هر مدل محتوا یک فیلد is_published دارد
            # این بخش باید متناسب با ساختار پروژه شما تنظیم شود
            published_content = 0
            for model in content_models:
                if hasattr(model, 'is_published'):
                    published_content += model.objects.filter(is_published=True).count()
                elif hasattr(model, 'status'):
                    published_content += model.objects.filter(status='published').count()
            
            content_percentage = int((published_content / total_content) * 100) if total_content > 0 else 0
        except Exception as e:
            # در صورت بروز خطا مقادیر پیش‌فرض استفاده می‌شود
            total_content = 0
            published_content = 0
            content_percentage = 0
        
        # فعالیت‌های اخیر
        recent_actions = LogEntry.objects.select_related('content_type', 'user')[:10]
        formatted_actions = []
        for action in recent_actions:
            formatted_actions.append({
                'message': f"{action.user.username} {action.get_action_flag_display()} {action.object_repr}",
                'timestamp': action.action_time
            })
        
        # اطلاعات سیستم
        django_version = get_version()
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        database_engine = connection.vendor
        
        context.update({
            'total_users': total_users,
            'active_users': active_users,
            'user_percentage': user_percentage,
            'total_content': total_content,
            'published_content': published_content,
            'content_percentage': content_percentage,
            'recent_actions': formatted_actions,
            'django_version': django_version,
            'python_version': python_version,
            'database_engine': database_engine,
        })
        
        return context 