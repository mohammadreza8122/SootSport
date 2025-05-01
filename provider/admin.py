# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# فرض می‌کنیم مدل‌ها در فایلی به نام models.py در همین اپلیکیشن قرار دارند
from .models import (
    Category, Tag, SportFacility, FacilityImage, Feature, Drawback,
    OptionalService, Discount, TimeSlot, Reservation
)
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline, TabularInline


# تنظیمات ساده برای مدل‌های Category و Tag
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # اسلاگ به صورت خودکار از نام ساخته می‌شود

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Inlines برای نمایش و ویرایش مدل‌های وابسته در صفحه SportFacility
class FacilityImageInline(TabularInline): # یا StackedInline برای نمایش عمودی
    model = FacilityImage
    tab=True
    extra = 1 # تعداد فرم خالی برای اضافه کردن تصویر جدید
    readonly_fields = ('image_preview',) # نمایش پیش‌نمایش تصویر (نیاز به تعریف متد دارد)
    fields = ('image', 'image_preview', 'caption', 'is_cover')

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return _("بدون تصویر")
    image_preview.short_description = _("پیش‌نمایش")

class FeatureInline(TabularInline):
    model = Feature
    extra = 1
    tab=True


class DrawbackInline(TabularInline):
    model = Drawback
    extra = 1
    tab=True


class OptionalServiceInline(TabularInline):
    model = OptionalService
    extra = 1
    tab=True

    fields = ('name', 'price', 'description')

class TimeSlotInline(TabularInline): # نمایش سانس‌ها در صفحه سالن
    model = TimeSlot
    tab=True

    extra = 0 # معمولا سانس‌ها به صورت انبوه ساخته می‌شوند، نه تکی اینجا
    fields = ('date', 'start_time', 'end_time', 'base_price', 'discount', 'is_available')
    ordering = ('date', 'start_time')
    # می‌توان فیلترهای بیشتری اضافه کرد
    # readonly_fields = ('get_final_price',) # برای نمایش قیمت نهایی در ادمین

    # def get_final_price(self, obj):
    #     return obj.get_final_price()
    # get_final_price.short_description = _("قیمت نهایی")

# تنظیمات اصلی برای مدل SportFacility
@admin.register(SportFacility)
class SportFacilityAdmin(ModelAdmin):
    list_display = ('name', 'category', 'gender_type', 'is_active', 'created_at')
    list_filter = ('category', 'gender_type', 'is_active', 'tags')
    search_fields = ('name', 'description', 'address', 'category__name', 'tags__name')
    list_editable = ('is_active',)
    inlines = [
        FacilityImageInline,
        FeatureInline,
        DrawbackInline,
        OptionalServiceInline,
        TimeSlotInline, # نمایش و مدیریت سانس‌های مرتبط
    ]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'address', 'gender_type', 'is_active')
        }),
        (_("تگ‌ها و زمان‌ها"), {
            'fields': ('tags', ('created_at', 'updated_at'))
        }),
        # می‌توان بخش‌های دیگری برای فیلدهای اضافی اضافه کرد
    )
    filter_horizontal = ('tags',) # نمایش بهتر برای فیلدهای ManyToManyField

# تنظیمات برای مدل Discount
@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = ('description', 'code', 'discount_type', 'value', 'start_date', 'end_date', 'is_active', 'used_count', 'usage_limit')
    list_filter = ('discount_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('code', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('used_count',)
    fieldsets = (
        (None, {
            'fields': ('description', 'code', 'discount_type', 'value', 'max_discount_amount')
        }),
        (_("اعتبار و محدودیت"), {
            'fields': ('start_date', 'end_date', 'usage_limit', 'used_count', 'is_active')
        }),
    )

# تنظیمات برای مدل TimeSlot
@admin.register(TimeSlot)
class TimeSlotAdmin(ModelAdmin):
    list_display = ('facility', 'date', 'start_time', 'end_time', 'base_price', 'discount', 'is_available', 'get_final_price_display')
    list_filter = ('date', 'is_available', 'facility__category', 'facility')
    search_fields = ('facility__name', 'date')
    list_editable = ('is_available', 'base_price', 'discount')
    autocomplete_fields = ('facility', 'discount') # اگر تعداد سالن‌ها یا تخفیف‌ها زیاد است
    date_hierarchy = 'date' # نوار ناوبری بر اساس تاریخ بالای لیست
    ordering = ('date', 'start_time')

    # متد برای نمایش قیمت نهایی در لیست
    def get_final_price_display(self, obj):
        return obj.get_final_price()
    get_final_price_display.short_description = _("قیمت نهایی")
    get_final_price_display.admin_order_field = 'base_price' # قابلیت مرتب‌سازی بر اساس قیمت پایه


# Inline برای نمایش آپشن‌های انتخابی در صفحه Reservation
class SelectedOptionalServiceInline(TabularInline):
    tab=True

    model = Reservation.selected_optional_services.through # استفاده از مدل واسط ManyToMany
    verbose_name = _("آپشن انتخابی")
    verbose_name_plural = _("آپشن‌های انتخابی")
    extra = 0
    # autocomplete_fields = ('optionalservice',) # اگر تعداد آپشن‌ها زیاد است

# تنظیمات برای مدل Reservation
@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    list_display = ('id','user_display', 'time_slot_display', 'status', 'final_price', 'reservation_time', 'payment_time')
    list_filter = ('status', 'reservation_time', 'time_slot__date', 'time_slot__facility')
    search_fields = ('user__username', 'user__email', 'time_slot__facility__name', 'applied_discount_code', 'id')
    readonly_fields = ('user', 'time_slot', 'final_price', 'applied_discount_code', 'reservation_time', 'payment_time', 'selected_optional_services') # این فیلدها معمولا بعد از ایجاد نباید دستی تغییر کنند
    autocomplete_fields = ('user', 'time_slot') # برای انتخاب راحت‌تر کاربر و سانس
    date_hierarchy = 'reservation_time'
    ordering = ('-reservation_time',)
    # inlines = [SelectedOptionalServiceInline,] # نمایش آپشن های انتخاب شده

    fieldsets = (
        (None, {
            'fields': ('user', 'time_slot', 'status')
        }),
        (_("جزئیات مالی و زمانی"), {
            'fields': ('final_price', 'applied_discount_code', 'reservation_time', 'payment_time')
        }),
        (_("سایر اطلاعات"), {
            'fields': ('notes', 'selected_optional_services') # نمایش آپشن های انتخاب شده به صورت فقط خواندنی
        }),
    )

    # متدهای کمکی برای نمایش بهتر در لیست
    def user_display(self, obj):
        return obj.user.get_username()
    user_display.short_description = _("کاربر")
    user_display.admin_order_field = 'user'

    def time_slot_display(self, obj):
        return str(obj.time_slot)
    time_slot_display.short_description = _("سانس")
    time_slot_display.admin_order_field = 'time_slot'

    # actions = ['mark_as_confirmed', 'mark_as_cancelled'] # می‌توان Actionهایی برای تغییر وضعیت گروهی اضافه کرد

    # def mark_as_confirmed(self, request, queryset):
    #     # منطق تایید کردن رزروها و احتمالا تغییر وضعیت سانس
    #     queryset.update(status='C', payment_time=timezone.now()) # نیاز به ایمپورت timezone
    #     # اینجا باید منطق is_available سانس هم آپدیت شود (مثلا با حلقه زدن روی queryset)
    # mark_as_confirmed.short_description = _("علامت زدن به عنوان تایید شده")

    # def mark_as_cancelled(self, request, queryset):
    #     # منطق لغو کردن رزروها و احتمالا تغییر وضعیت سانس
    #     queryset.update(status='X')
    #      # اینجا باید منطق is_available سانس هم آپدیت شود
    # mark_as_cancelled.short_description = _("علامت زدن به عنوان لغو شده")

# عدم نیاز به ثبت مدل‌های Inline به صورت جداگانه
# admin.site.register(FacilityImage)
# admin.site.register(Feature)
# admin.site.register(Drawback)
# admin.site.register(OptionalService)