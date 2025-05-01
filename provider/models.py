# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime

class Category(models.Model):
    name = models.CharField(_("نام دسته‌بندی"), max_length=100, unique=True)
    slug = models.SlugField(_("اسلاگ (نامک)"), max_length=110, unique=True, help_text=_("برای استفاده در URLها، معمولا نسخه لاتین و خط‌فاصله‌دار نام است."))
    description = models.TextField(_("توضیحات"), blank=True, null=True)

    class Meta:
        verbose_name = _("دسته‌بندی")
        verbose_name_plural = _("دسته‌بندی‌ها")
        ordering = ['name']

    def __str__(self):
        return self.name

# مدل تگ‌ها (مثلا: سرپوشیده، چمن مصنوعی، دارای پارکینگ)
class Tag(models.Model):
    name = models.CharField(_("نام تگ"), max_length=100, unique=True)
    slug = models.SlugField(_("اسلاگ (نامک)"), max_length=110, unique=True)

    class Meta:
        verbose_name = _("تگ")
        verbose_name_plural = _("تگ‌ها")
        ordering = ['name']

    def __str__(self):
        return self.name

# مدل سالن ورزشی
class SportFacility(models.Model):
    GENDER_CHOICES = [
        ('M', _('آقایان')),
        ('F', _('بانوان')),
        ('B', _('آقایان و بانوان (مشترک با سانس‌های جداگانه)')),
    ]

    name = models.CharField(_("نام سالن"), max_length=200)
    description = models.TextField(_("توضیحات کامل"))
    address = models.CharField(_("آدرس"), blank=True, null=True, max_length=200)
    city = models.ForeignKey('address.City', on_delete=models.CASCADE, related_name='facilities', verbose_name=_("شهر"), null=True)
    province = models.ForeignKey('address.Province', on_delete=models.CASCADE, related_name='facilities', verbose_name=_("ا��تان"), null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='facilities', verbose_name=_("دسته‌بندی"))
    tags = models.ManyToManyField(Tag, blank=True, related_name='facilities', verbose_name=_("تگ‌ها"))
    gender_type = models.CharField(_("مخصوص"), max_length=1, choices=GENDER_CHOICES, default='B')
    is_active = models.BooleanField(_("فعال"), default=True, help_text=_("آیا این سالن برای رزرو نمایش داده شود؟"))
    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("زمان بروزرسانی"), auto_now=True)
    # فیلدهای دیگر مثل موقعیت جغرافیایی (latitude, longitude)، ظرفیت، قوانین و ...

    class Meta:
        verbose_name = _("سالن ورزشی")
        verbose_name_plural = _("سالن‌های ورزشی")
        ordering = ['name']

    def __str__(self):
        return self.name

# مدل گالری تصاویر برای هر سالن
class FacilityImage(models.Model):
    UPLOADED_BY = (('admin', 'ادمین'), ('user', 'کاربر'))
    uploaded_by = models.CharField(_("��پلود شده بوسیله"), max_length=50, choices=UPLOADED_BY, default='admin')
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name='images', verbose_name=_("سالن ورزشی"))
    image = models.ImageField(_("تصویر"), upload_to='facility_images/')
    caption = models.CharField(_("عنوان تصویر"), max_length=200, blank=True, null=True)
    is_cover = models.BooleanField(_("تصویر کاور"), default=False, help_text=_("آیا این تصویر اصلی سالن است؟"))
    alt_text = models.CharField(_("متن جایگزین تصویر"), max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = _("تصویر سالن")
        verbose_name_plural = _("گالری تصاویر سالن")
        ordering = ['-is_cover', 'id'] # کاور اول نمایش داده شود

    def __str__(self):
        return f"{self.facility.name} - {self.caption or 'Image'}"

# مدل ویژگی‌های مثبت (امکانات)
class Feature(models.Model):
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name='features', verbose_name=_("سالن ورزشی"))
    text = models.CharField(_("متن ویژگی"), max_length=255)

    class Meta:
        verbose_name = _("ویژگی مثبت (امکانات)")
        verbose_name_plural = _("ویژگی‌های مثبت (امکانات)")

    def __str__(self):
        return f"{self.facility.name} - {self.text}"

# مدل ویژگی‌های منفی (معایب)
class Drawback(models.Model):
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name='drawbacks', verbose_name=_("سالن ورزشی"))
    text = models.CharField(_("متن عیب"), max_length=255)

    class Meta:
        verbose_name = _("ویژگی منفی (عیب)")
        verbose_name_plural = _("ویژگی‌های منفی (معایب)")

    def __str__(self):
        return f"{self.facility.name} - {self.text}"

# مدل آپشن‌های انتخابی اضافی (مثل اجاره توپ، لباس و ...)
class OptionalService(models.Model):
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name='optional_services', verbose_name=_("سالن ورزشی"))
    name = models.CharField(_("نام آپشن"), max_length=150)
    price = models.DecimalField(_("قیمت آپشن"), max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal('0.00'))])
    description = models.TextField(_("توضیحات آپشن"), blank=True, null=True)

    class Meta:
        verbose_name = _("آپشن انتخابی")
        verbose_name_plural = _("آپشن‌های انتخابی")
        unique_together = ('facility', 'name') # هر آپشن برای هر سالن باید نام منحصر به فرد داشته باشد

    def __str__(self):
        return f"{self.facility.name} - {self.name} ({self.price})"

# مدل تخفیف‌ها
class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('P', _('درصدی')),
        ('F', _('مبلغ ثابت')),
    ]
    code = models.CharField(_("کد تخفیف"), max_length=50, unique=True, blank=True, null=True, help_text=_("اگر خالی باشد، تخفیف به صورت خودکار اعمال می‌شود (مثلا برای یک سانس خاص)."))
    description = models.CharField(_("توضیحات تخفیف"), max_length=255)
    discount_type = models.CharField(_("نوع تخفیف"), max_length=1, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(_("مقدار تخفیف"), max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text=_("اگر درصدی است عدد بین 0 تا 100، اگر ثابت است مبلغ به تومان"))
    max_discount_amount = models.DecimalField(_("حداکثر مبلغ تخفیف (برای نوع درصدی)"), max_digits=10, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    start_date = models.DateTimeField(_("تاریخ شروع اعتبار"), blank=True, null=True)
    end_date = models.DateTimeField(_("تاریخ پایان اعتبار"), blank=True, null=True)
    usage_limit = models.PositiveIntegerField(_("محدودیت تعداد استفاده"), blank=True, null=True)
    used_count = models.PositiveIntegerField(_("تعداد استفاده شده"), default=0, editable=False)
    is_active = models.BooleanField(_("فعال"), default=True)

    # می‌توان محدودیت‌هایی برای کاربر، دسته‌بندی خاص یا سالن خاص هم اضافه کرد

    class Meta:
        verbose_name = _("تخفیف")
        verbose_name_plural = _("تخفیف‌ها")

    def __str__(self):
        return self.description or self.code or f"Discount {self.id}"

    def is_valid(self):
        now = datetime.datetime.now(datetime.timezone.utc) # یا timezone.now() در جنگو
        if not self.is_active:
            return False
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        return True

# مدل سانس (نوبت زمانی)
class TimeSlot(models.Model):
    GENDER_CHOICES = [
        ('M', _('آقایان')),
        ('F', _('بانوان')),
    ]
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name='time_slots', verbose_name=_("سالن ورزشی"))
    date = models.DateField(_("تاریخ"))
    start_time = models.TimeField(_("زمان شروع"))
    end_time = models.TimeField(_("زمان پایان"))
    base_price = models.DecimalField(_("قیمت پایه"), max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal('0.00'))])
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True, related_name='time_slots', verbose_name=_("تخفیف اختصاصی سانس"))
    is_available = models.BooleanField(_("در دسترس برای رزرو"), default=True)
    gender_type = models.CharField(_("مخصوص"), max_length=1, choices=GENDER_CHOICES, default='B')

    # می‌توان فیلد gender_restriction مخصوص این سانس هم گذاشت اگر با gender_type سالن متفاوت باشد

    class Meta:
        verbose_name = _("سانس (نوبت زمانی)")
        verbose_name_plural = _("سانس‌ها")
        ordering = ['date', 'start_time']
        unique_together = ('facility', 'date', 'start_time') # هر سانس در یک روز و ساعت برای یک سالن منحصر به فرد است
        # می‌توان محدودیت (constraint) گذاشت که end_time حتما بعد از start_time باشد

    def __str__(self):
        return f"{self.facility.name} - {self.date} - {self.start_time.strftime('%H:%M')} تا {self.end_time.strftime('%H:%M')}"

    def get_final_price(self):
        """محاسبه قیمت نهایی با در نظر گرفتن تخفیف اختصاصی سانس"""
        price = self.base_price
        if self.discount and self.discount.is_valid():
            if self.discount.discount_type == 'P': # درصدی
                discount_amount = (self.discount.value / Decimal('100')) * price
                if self.discount.max_discount_amount and discount_amount > self.discount.max_discount_amount:
                    discount_amount = self.discount.max_discount_amount
                price -= discount_amount
            elif self.discount.discount_type == 'F': # مبلغ ثابت
                price -= self.discount.value
            if price < 0:
                price = Decimal('0')
        return price.quantize(Decimal('0')) # رند کردن به عدد صحیح (تومان)

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('P', _('در انتظار پرداخت')),
        ('C', _('تایید شده')),
        ('X', _('لغو شده')),
        ('E', _('منقضی شده')), # اگر پرداخت انجام نشود
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reservations', verbose_name=_("کاربر"))
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='reservations', verbose_name=_("سانس رزرو شده"))
    status = models.CharField(_("وضعیت رزرو"), max_length=1, choices=STATUS_CHOICES, default='P')
    # قیمت نهایی در زمان رزرو ثبت می‌شود تا با تغییرات بعدی قیمت سانس یا تخفیف، سابقه حفظ شود
    final_price = models.DecimalField(_("مبلغ نهایی پرداخت شده/پرداختنی"), max_digits=10, decimal_places=0)
    applied_discount_code = models.CharField(_("کد تخفیف استفاده شده"), max_length=50, blank=True, null=True) # اگر کاربر کد تخفیف جداگانه وارد کرد
    # آپشن‌های انتخابی که کاربر برای این رزرو خاص انتخاب کرده
    selected_optional_services = models.ManyToManyField(OptionalService, blank=True, related_name='reservations', verbose_name=_("آپشن‌های انتخابی رزرو"))
    reservation_time = models.DateTimeField(_("زمان ثبت رزرو"), auto_now_add=True)
    payment_time = models.DateTimeField(_("زمان پرداخت"), blank=True, null=True)
    notes = models.TextField(_("یادداشت کاربر"), blank=True, null=True)

    class Meta:
        verbose_name = _("رزرو")
        verbose_name_plural = _("رزروها")
        ordering = ['-reservation_time']

    def __str__(self):
        return f"رزرو {self.user.get_username()} برای {self.time_slot}"
