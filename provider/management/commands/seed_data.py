# -*- coding: utf-8 -*-
import random
import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

# مدل‌های خود را از اپلیکیشن مربوطه ایمپورت کنید
# فرض می‌کنیم اپلیکیشن شما 'reservations' نام دارد
from provider.models import (Category, Tag, SportFacility, FacilityImage, Feature, Drawback,
    OptionalService, Discount, TimeSlot, Reservation)


User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample data for the sports reservation system.'

    # می‌توانید با استفاده از add_arguments پارامترهایی برای دستور تعریف کنید
    # مثلا تعداد رکوردهایی که باید ایجاد شود

    @transaction.atomic  # برای اطمینان از اینکه تمام عملیات با هم انجام یا لغو شوند
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        # به ترتیب معکوس وابستگی‌ها حذف کنید
        Reservation.objects.all().delete()
        TimeSlot.objects.all().delete()
        OptionalService.objects.all().delete()
        Drawback.objects.all().delete()
        Feature.objects.all().delete()
        FacilityImage.objects.all().delete() # فقط رکوردها حذف می‌شوند، نه فایل‌های واقعی
        SportFacility.objects.all().delete()
        Discount.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        # User.objects.filter(is_superuser=False).delete() # کاربران عادی را حذف کنید؟ (اختیاری)

        self.stdout.write(self.style.SUCCESS('Creating new data...'))

        # --- 1. ایجاد کاربران تست ---
        users = []
        user1, created = User.objects.get_or_create(
            phone_number='0921243454523',
            defaults={'email': 'user1@example.com', 'first_name': 'کاربر', 'last_name': 'تستی ۱'}
        )
        if created:
            user1.set_password('password123')
            user1.save()
        users.append(user1)

        user2, created = User.objects.get_or_create(
            phone_number='0934235465667',
            defaults={'email': 'user2@example.com', 'first_name': 'کاربر', 'last_name': 'تستی ۲'}
        )
        if created:
            user2.set_password('password123')
            user2.save()
        users.append(user2)
        self.stdout.write(f'{len(users)} test users created/found.')

        # --- 2. ایجاد دسته‌بندی‌ها ---
        categories_data = [
            {'name': 'فوتسال', 'slug': 'futsal'},
            {'name': 'والیبال', 'slug': 'volleyball'},
            {'name': 'بسکتبال', 'slug': 'basketball'},
            {'name': 'استخر', 'slug': 'pool'},
            {'name': 'تنیس', 'slug': 'tennis'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(**cat_data)
            categories.append(cat)
        self.stdout.write(f'{len(categories)} categories created/found.')

        # --- 3. ایجاد تگ‌ها ---
        tags_data = [
            {'name': 'سرپوشیده', 'slug': 'indoor'},
            {'name': 'روباز', 'slug': 'outdoor'},
            {'name': 'چمن مصنوعی', 'slug': 'artificial-grass'},
            {'name': 'کفپوش سالنی', 'slug': 'hardwood-floor'},
            {'name': 'دارای پارکینگ', 'slug': 'parking-available'},
            {'name': 'دوش و رختکن', 'slug': 'showers-lockers'},
            {'name': 'مناسب کودکان', 'slug': 'kid-friendly'},
        ]
        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)
        self.stdout.write(f'{len(tags)} tags created/found.')

        # --- 4. ایجاد تخفیف‌ها ---
        now = timezone.now()
        discounts = []
        d1, _ = Discount.objects.get_or_create(
            code='BAHAR1404',
            defaults={
                'description': 'تخفیف 15% بهاری',
                'discount_type': 'P',
                'value': Decimal('15.00'),
                'start_date': now - datetime.timedelta(days=10),
                'end_date': now + datetime.timedelta(days=20),
                'is_active': True,
                'usage_limit': 100
            }
        )
        discounts.append(d1)

        d2, _ = Discount.objects.get_or_create(
            code=None, # تخفیف بدون کد، مثلا برای سانس خاص
             defaults={
                'description': 'تخفیف 20 هزار تومانی سانس صبح',
                'discount_type': 'F',
                'value': Decimal('20000'),
                'is_active': True,
                'start_date': now - datetime.timedelta(days=30),
                # 'end_date': None # بدون تاریخ انقضا
            }
        )
        discounts.append(d2)

        d3, _ = Discount.objects.get_or_create(
            code='EXPIRED',
             defaults={
                'description': 'تخفیف منقضی شده',
                'discount_type': 'P',
                'value': Decimal('10.00'),
                'start_date': now - datetime.timedelta(days=60),
                'end_date': now - datetime.timedelta(days=30),
                'is_active': False # منقضی شده
            }
        )
        # discounts.append(d3) # از تخفیف منقضی شده استفاده نمی‌کنیم
        self.stdout.write(f'{len(discounts)} active discounts created/found.')

        # --- 5. ایجاد سالن‌های ورزشی ---
        facilities = []
        facility_names = [
            "مجموعه ورزشی آزادی", "سالن حجاب", "باشگاه انقلاب", "زمین چمن آرارات",
            "استخر شهید کشوری", "سالن بسکتبال اکباتان", "زمین تنیس استقلال"
        ]
        addresses = ["تهران، ...", "اصفهان، ...", "شیراز، ..."]
        descriptions = [
            "یک سالن مجهز با امکانات کامل.",
            "مناسب برای تمرین و مسابقات دوستانه.",
            "محیطی آرام و خانوادگی برای ورزش.",
            "دارای بهترین کیفیت چمن/کفپوش.",
        ]

        for i in range(5): # ایجاد 5 سالن تست
            facility_data = {
                'name': f"{random.choice(facility_names)} - {i+1}",
                'category': random.choice(categories),
                'description': random.choice(descriptions),
                'address': random.choice(addresses),
                'gender_type': random.choice(['M', 'F', 'B']),
                'is_active': True,
            }
            facility, _ = SportFacility.objects.get_or_create(name=facility_data['name'], defaults=facility_data)

            # اضافه کردن تگ‌های تصادفی
            num_tags = random.randint(1, 4)
            facility.tags.set(random.sample(tags, num_tags))

            facilities.append(facility)

            # --- 6. ایجاد ویژگی‌ها، معایب و آپشن‌ها برای هر سالن ---
            features_texts = ["پارکینگ رایگان", "بوفه", "سیستم تهویه مطبوع", "جایگاه تماشاچی"]
            for _ in range(random.randint(1, 3)):
                Feature.objects.create(facility=facility, text=random.choice(features_texts))

            drawbacks_texts = ["عدم وجود آب سردکن", "نور کم در شب", "دسترسی سخت با وسایل عمومی"]
            if random.random() < 0.5: # 50% شانس داشتن عیب
                 for _ in range(random.randint(0, 2)):
                    Drawback.objects.create(facility=facility, text=random.choice(drawbacks_texts))

            options_data = [
                {'name': 'اجاره توپ', 'price': Decimal('10000')},
                {'name': 'اجاره راکت', 'price': Decimal('25000')},
                {'name': 'حوله', 'price': Decimal('5000')},
                {'name': 'کمد اختصاصی', 'price': Decimal('15000')},
            ]
            num_options = random.randint(1, 3)
            selected_options = random.sample(options_data, num_options)
            for opt_data in selected_options:
                OptionalService.objects.create(facility=facility, **opt_data)

            # نکته: ایجاد FacilityImage نیاز به فایل تصویری دارد.
            # برای سادگی، در این اسکریپت ایجاد نمی‌کنیم.
            # می‌توانید تصاویر پیش‌فرض را در پوشه media قرار دهید و مسیر آنها را بدهید
            # یا از کتابخانه‌هایی مثل Factory Boy استفاده کنید که می‌توانند فایل‌های جعلی بسازند.

        self.stdout.write(f'{len(facilities)} facilities created/found.')
        self.stdout.write('Features, Drawbacks, Optional Services added.')

        # --- 7. ایجاد سانس‌ها ---
        time_slots_created = 0
        available_slots_for_reservation = []
        start_times = [datetime.time(h, 0) for h in range(8, 22)] # از ۸ صبح تا ۱۰ شب

        for facility in facilities:
            base_price = Decimal(random.randint(10, 50) * 10000) # قیمت بین ۱۰۰ هزار تا ۵۰۰ هزار تومان
            for day_offset in range(7): # سانس برای ۷ روز آینده
                current_date = (now + datetime.timedelta(days=day_offset)).date()
                for i in range(len(start_times) - 1):
                    # شانس 70% برای ایجاد سانس در این زمان
                    if random.random() < 0.7:
                        start_time = start_times[i]
                        end_time = start_times[i+1] # فرض می‌کنیم سانس‌ها یک ساعته هستند

                        # شانس 20% برای داشتن تخفیف اختصاصی سانس (از تخفیف‌های فعال)
                        slot_discount = None
                        if random.random() < 0.2 and discounts:
                            slot_discount = random.choice([d for d in discounts if d.is_valid()])

                        # شانس 80% برای در دسترس بودن سانس
                        is_available = random.random() < 0.8

                        slot, created = TimeSlot.objects.get_or_create(
                            facility=facility,
                            date=current_date,
                            start_time=start_time,
                            defaults={
                                'end_time': end_time,
                                'base_price': base_price + Decimal(random.randint(-2, 5) * 10000), # کمی تنوع قیمت
                                'discount': slot_discount,
                                'is_available': is_available
                            }
                        )
                        if created:
                            time_slots_created += 1
                            if is_available:
                                available_slots_for_reservation.append(slot)
                            # اگر سانس در دسترس نبود، لازم نیست کاری کنیم چون پیش‌فرض رزرو نشده

        self.stdout.write(f'{time_slots_created} time slots created.')

        # --- 8. ایجاد رزروها ---
        reservations_created = 0
        num_reservations = min(len(available_slots_for_reservation), 30) # حداکثر ۳۰ رزرو ایجاد کن

        # مطمئن شویم که اسلات‌های کافی داریم
        if not available_slots_for_reservation:
             self.stdout.write(self.style.WARNING('No available time slots found to create reservations.'))

        else:
            # اسلات‌های قابل رزرو را به صورت تصادفی انتخاب می‌کنیم تا تکراری نباشند
            slots_to_reserve = random.sample(available_slots_for_reservation, k=min(len(available_slots_for_reservation), num_reservations))


            for slot in slots_to_reserve:
                user = random.choice(users)
                status = random.choice(['P', 'C', 'C', 'C']) # شانس بیشتر برای تایید شده

                # محاسبه قیمت نهایی اولیه (ممکن است کد تخفیف کاربر هم اعمال شود)
                final_price = slot.get_final_price()
                applied_discount_code = slot.discount.code if slot.discount and slot.discount.code else None

                # شانس 15% برای استفاده از کد تخفیف عمومی کاربر
                user_discount = None
                if random.random() < 0.15:
                     active_coded_discounts = [d for d in discounts if d.code and d.is_valid()]
                     if active_coded_discounts:
                         user_discount = random.choice(active_coded_discounts)
                         # محاسبه مجدد قیمت با تخفیف کاربر
                         if user_discount.discount_type == 'P':
                             discount_amount = (user_discount.value / Decimal('100')) * final_price
                             if user_discount.max_discount_amount and discount_amount > user_discount.max_discount_amount:
                                 discount_amount = user_discount.max_discount_amount
                             final_price -= discount_amount
                         elif user_discount.discount_type == 'F':
                              final_price -= user_discount.value
                         if final_price < 0: final_price = Decimal('0')
                         applied_discount_code = user_discount.code # کد کاربر اولویت دارد

                reservation_data = {
                    'user': user,
                    'time_slot': slot,
                    'status': status,
                    'final_price': final_price.quantize(Decimal('0')),
                    'applied_discount_code': applied_discount_code,
                    'notes': random.choice(["", "رزرو تستی", "نیاز به توپ اضافه"]) if random.random() < 0.3 else ""
                }

                # اگر رزرو تایید شده، زمان پرداخت را ثبت کن و سانس را غیرفعال کن
                payment_time = None
                if status == 'C':
                    payment_time = timezone.now() - datetime.timedelta(minutes=random.randint(5, 120))
                    reservation_data['payment_time'] = payment_time
                    slot.is_available = False
                    slot.save() # ذخیره تغییر وضعیت سانس

                    # افزایش شمارنده استفاده از کد تخفیف در صورت وجود
                    if user_discount and user_discount.usage_limit is not None:
                         user_discount.used_count += 1
                         user_discount.save()
                    elif slot.discount and slot.discount.usage_limit is not None:
                         slot.discount.used_count += 1
                         slot.discount.save()


                reservation = Reservation.objects.create(**reservation_data)

                # اضافه کردن آپشن‌های انتخابی تصادفی به رزرو
                facility_options = OptionalService.objects.filter(facility=slot.facility)
                if facility_options.exists():
                    num_selected_options = random.randint(0, facility_options.count())
                    if num_selected_options > 0:
                        selected_services = random.sample(list(facility_options), num_selected_options)
                        reservation.selected_optional_services.set(selected_services)
                        # نکته: در مدل واقعی باید قیمت این آپشن‌ها به final_price اضافه شود (اینجا ساده‌سازی شده)

                reservations_created += 1

            self.stdout.write(f'{reservations_created} reservations created.')

        self.stdout.write(self.style.SUCCESS('Database seeding finished successfully!'))