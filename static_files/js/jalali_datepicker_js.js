// اسکریپت برای مدیریت تقویم شمسی در پنل ادمین جنگو

document.addEventListener('DOMContentLoaded', function() {
    loadJalaliDatePickerResources();
});

// بارگذاری منابع مورد نیاز برای تقویم شمسی
function loadJalaliDatePickerResources() {
    // بررسی اینکه آیا منابع قبلاً بارگذاری شده‌اند
    if (typeof persianDate !== 'undefined' && typeof $ !== 'undefined' && typeof $.fn.pDatepicker !== 'undefined') {
        initAllJalaliDatePickers();
        return;
    }

    // بارگذاری jQuery اگر در دسترس نیست
    if (typeof $ === 'undefined') {
        var jqueryScript = document.createElement('script');
        jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js';
        jqueryScript.onload = function() {
            loadPersianDateScript();
        };
        document.head.appendChild(jqueryScript);
    } else {
        loadPersianDateScript();
    }
}

// بارگذاری کتابخانه PersianDate
function loadPersianDateScript() {
    var persianDateScript = document.createElement('script');
    persianDateScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/persian-date/1.1.0/persian-date.min.js';
    persianDateScript.onload = function() {
        loadPersianDatePickerScript();
    };
    document.head.appendChild(persianDateScript);
}

// بارگذاری کتابخانه PersianDatepicker
function loadPersianDatePickerScript() {
    // بارگذاری CSS
    var datePickerCSS = document.createElement('link');
    datePickerCSS.rel = 'stylesheet';
    datePickerCSS.href = 'https://cdnjs.cloudflare.com/ajax/libs/persian-datepicker/1.2.0/css/persian-datepicker.min.css';
    document.head.appendChild(datePickerCSS);

    // بارگذاری JavaScript
    var datePickerScript = document.createElement('script');
    datePickerScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/persian-datepicker/1.2.0/js/persian-datepicker.min.js';
    datePickerScript.onload = function() {
        initAllJalaliDatePickers();
    };
    document.head.appendChild(datePickerScript);
}

// راه‌اندازی همه انتخابگرهای تاریخ شمسی در صفحه
function initAllJalaliDatePickers() {
    // پیکربندی برای همه فیلدهای تاریخ
    var dateInputs = document.querySelectorAll('.jalali-datepicker');
    dateInputs.forEach(function(input) {
        initJalaliDatePicker(input.id);
    });

    // پیکربندی برای همه فیلدهای تاریخ و زمان
    var dateTimeInputs = document.querySelectorAll('.jalali-datetimepicker');
    dateTimeInputs.forEach(function(input) {
        initJalaliDateTimePicker(input.id);
    });

    // جایگزینی تقویم شمسی برای همه فیلدهای تاریخ جنگو (برای سازگاری با ویجت‌های موجود)
    replaceDefaultDatePickers();
}

// راه‌اندازی انتخابگر تاریخ شمسی برای یک فیلد خاص
function initJalaliDatePicker(inputId) {
    if (!inputId || typeof $ === 'undefined' || typeof $.fn.pDatepicker === 'undefined') return;

    var $input = $('#' + inputId);
    if ($input.length === 0) return;

    $input.pDatepicker({
        format: 'YYYY/MM/DD',
        autoClose: true,
        initialValueType: 'gregorian',
        calendar: {
            persian: {
                locale: 'fa'
            }
        },
        onSelect: function(dateText) {
            // تبدیل تاریخ شمسی به میلادی برای ارسال به سرور
            var pd = $input.pDatepicker('getDate');
            var gDate = pd.gDate;
            
            // برای سازگاری با جنگو، مقدار hidden ایجاد می‌کنیم
            var hiddenId = inputId + '_hidden';
            var $hidden = $('#' + hiddenId);
            
            if ($hidden.length === 0) {
                $hidden = $('<input>').attr({
                    type: 'hidden',
                    id: hiddenId,
                    name: $input.attr('name')
                });
                $input.after($hidden);
                // تغییر name اصلی برای جلوگیری از ارسال دو مقدار
                $input.attr('name', $input.attr('name') + '_display');
            }
            
            // فرمت تاریخ میلادی متناسب با Django
            var year = gDate.getFullYear();
            var month = ('0' + (gDate.getMonth() + 1)).slice(-2);
            var day = ('0' + gDate.getDate()).slice(-2);
            
            $hidden.val(year + '-' + month + '-' + day);
        }
    });
}

// راه‌اندازی انتخابگر تاریخ و زمان شمسی برای یک فیلد خاص
function initJalaliDateTimePicker(inputId) {
    if (!inputId || typeof $ === 'undefined' || typeof $.fn.pDatepicker === 'undefined') return;

    var $input = $('#' + inputId);
    if ($input.length === 0) return;

    $input.pDatepicker({
        format: 'YYYY/MM/DD HH:mm:ss',
        autoClose: true,
        timePicker: {
            enabled: true
        },
        initialValueType: 'gregorian',
        calendar: {
            persian: {
                locale: 'fa'
            }
        },
        onSelect: function(dateText) {
            // تبدیل تاریخ و زمان شمسی به میلادی برای ارسال به سرور
            var pd = $input.pDatepicker('getDate');
            var gDate = pd.gDate;
            
            // برای سازگاری با جنگو، مقدار hidden ایجاد می‌کنیم
            var hiddenId = inputId + '_hidden';
            var $hidden = $('#' + hiddenId);
            
            if ($hidden.length === 0) {
                $hidden = $('<input>').attr({
                    type: 'hidden',
                    id: hiddenId,
                    name: $input.attr('name')
                });
                $input.after($hidden);
                // تغییر name اصلی برای جلوگیری از ارسال دو مقدار
                $input.attr('name', $input.attr('name') + '_display');
            }
            
            // فرمت تاریخ و زمان میلادی متناسب با Django
            var year = gDate.getFullYear();
            var month = ('0' + (gDate.getMonth() + 1)).slice(-2);
            var day = ('0' + gDate.getDate()).slice(-2);
            var hours = ('0' + gDate.getHours()).slice(-2);
            var minutes = ('0' + gDate.getMinutes()).slice(-2);
            var seconds = ('0' + gDate.getSeconds()).slice(-2);
            
            $hidden.val(year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds);
        }
    });
}

// جایگزینی تقویم پیش‌فرض جنگو با تقویم شمسی
function replaceDefaultDatePickers() {
    // یافتن همه فیلدهای تاریخ جنگو که هنوز تبدیل نشده‌اند
    var defaultDateInputs = document.querySelectorAll('.vDateField:not(.jalali-datepicker)');
    defaultDateInputs.forEach(function(input) {
        // حذف کلاس پیش‌فرض و رویدادهای آن
        input.className = input.className.replace('vDateField', '');
        // اضافه کردن کلاس جدید
        input.classList.add('jalali-datepicker');
        // راه‌اندازی انتخابگر تاریخ شمسی
        initJalaliDatePicker(input.id);
    });

    // یافتن همه فیلدهای تاریخ و زمان جنگو که هنوز تبدیل نشده‌اند
    var defaultDateTimeInputs = document.querySelectorAll('.vDateTimeField:not(.jalali-datetimepicker)');
    defaultDateTimeInputs.forEach(function(input) {
        // حذف کلاس پیش‌فرض و رویدادهای آن
        input.className = input.className.replace('vDateTimeField', '');
        // اضافه کردن کلاس جدید
        input.classList.add('jalali-datetimepicker');
        // راه‌اندازی انتخابگر تاریخ و زمان شمسی
        initJalaliDateTimePicker(input.id);
    });
}
