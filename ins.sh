#!/bin/bash

# اسکریپت نصب برای پیاده‌سازی RTL و فارسی‌سازی

# ایجاد پوشه‌های مورد نیاز
echo "ایجاد پوشه‌های مورد نیاز..."
mkdir -p static_files/fonts
mkdir -p templates/admin

# دانلود فونت وزیر
echo "دانلود فونت وزیرمتن..."
curl -L "https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazirmatn-Regular.woff2" -o static_files/fonts/Vazirmatn-Regular.woff2
curl -L "https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazirmatn-Bold.woff2" -o static_files/fonts/Vazirmatn-Bold.woff2

# کپی فایل‌های CSS و JavaScript
echo "کپی فایل‌های استایل و اسکریپت..."
cp static/custom.css static_files/
cp static/custom.js static_files/

# اجرای collectstatic
echo "اجرای collectstatic..."
python manage.py collectstatic --noinput

echo "عملیات با موفقیت انجام شد!"
echo "برای اعمال تغییرات، سرور را مجدداً راه‌اندازی کنید."