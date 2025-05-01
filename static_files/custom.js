// اسکریپت سفارشی برای پشتیبانی بهتر RTL در جنگو انفولد

document.addEventListener('DOMContentLoaded', function() {
    applyRTLStyles();
    translateDarkModeToggle();

    // برای المان‌هایی که بعدا به DOM اضافه می‌شوند
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                applyRTLStyles();
                translateDarkModeToggle();
            }
        });
    });

    // پیکربندی و شروع observer
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// تابع جدید برای ترجمه متن تغییر حالت دارک مود
function translateDarkModeToggle() {
    // یافتن منوی تغییر تم با استفاده از سلکتور دقیق
    const themeMenu = document.querySelector('nav[x-show="openTheme"]');
    if (themeMenu) {
        // یافتن همه گزینه‌های داخل منو
        const themeOptions = themeMenu.querySelectorAll('a span.leading-none.self-center');

        themeOptions.forEach(option => {
            // ترجمه متن هر گزینه
            if (option.textContent === 'Dark') {
                option.textContent = 'تاریک';
            } else if (option.textContent === 'Light') {
                option.textContent = 'روشن';
            } else if (option.textContent === 'System') {
                option.textContent = 'سیستم';
            }
        });

        // اصلاح جهت آیکون‌ها (مواد)
        const materialIcons = themeMenu.querySelectorAll('.material-symbols-outlined');
        materialIcons.forEach(icon => {
            // تغییر مارجین از راست به چپ در حالت RTL
            if (document.dir === 'rtl' || document.documentElement.getAttribute('dir') === 'rtl') {
                icon.classList.remove('mr-2');
                icon.classList.add('ml-2');
            }
        });
    }

    // جستجو برای سایر المان‌های مرتبط با تغییر تم (مثل دکمه اصلی)
    const toggleButton = document.querySelector('[x-on\\:click="openTheme = !openTheme"]');
    if (toggleButton) {
        const buttonText = toggleButton.querySelector('span.leading-none.self-center');
        if (buttonText && buttonText.textContent.includes('Theme')) {
            buttonText.textContent = 'تم';
        }
    }
}

function applyRTLStyles() {
    // اصلاح جدول اصلی
    const resultList = document.getElementById('result_list');
    if (resultList) {
        resultList.style.direction = 'rtl';
        resultList.style.textAlign = 'right';

        // اصلاح سرستون‌ها
        const headers = resultList.querySelectorAll('th');
        headers.forEach(header => {
            header.style.textAlign = 'right';
        });

        // اصلاح سلول‌های جدول
        const cells = resultList.querySelectorAll('td');
        cells.forEach(cell => {
            cell.style.textAlign = 'right';
        });
    }

    // اصلاح فیلترها
    const filters = document.getElementById('changelist-filter');
    if (filters) {
        filters.style.direction = 'rtl';
        filters.style.textAlign = 'right';
    }

    // اصلاح فرم‌های داینامیک
    const inlineRelated = document.querySelectorAll('.inline-related');
    inlineRelated.forEach(item => {
        item.style.direction = 'rtl';
        item.style.textAlign = 'right';
    });

    // اصلاح پیام‌های سیستمی
    const messageList = document.querySelector('.messagelist');
    if (messageList) {
        messageList.style.direction = 'rtl';
        messageList.style.textAlign = 'right';

        const messages = messageList.querySelectorAll('li');
        messages.forEach(message => {
            message.style.direction = 'rtl';
            message.style.textAlign = 'right';
            message.style.paddingRight = '40px';
            message.style.paddingLeft = '10px';
            message.style.backgroundPosition = 'right 12px center';
        });
    }

    // اصلاح آیکون‌های متریال
    const materialIcons = document.querySelectorAll('.material-icons:not(.no-rtl)');
    materialIcons.forEach(icon => {
        icon.style.transform = 'scaleX(-1)';
    });

    // برای اصلاح select2 اگر استفاده می‌شود
    const select2Containers = document.querySelectorAll('.select2-container');
    select2Containers.forEach(container => {
        container.style.direction = 'rtl';
        container.style.textAlign = 'right';
    });

    // اصلاح تقویم و انتخاب‌گر زمان
    const calendarBox = document.querySelectorAll('.calendarbox, .clockbox');
    calendarBox.forEach(box => {
        box.style.direction = 'rtl';
        box.style.textAlign = 'right';
    });

    // اصلاح توضیحات راهنما
    const helpTexts = document.querySelectorAll('.help');
    helpTexts.forEach(help => {
        help.style.direction = 'rtl';
        help.style.textAlign = 'right';
    });

    // اصلاح تب‌های unfold
    const tabNavigation = document.querySelector('.tab-navigation');
    if (tabNavigation) {
        tabNavigation.style.direction = 'rtl';
        tabNavigation.style.textAlign = 'right';
    }

    // اصلاح بخش اصلی محتوا
    const contentContainer = document.querySelector('.content-container');
    if (contentContainer) {
        contentContainer.style.direction = 'rtl';
        contentContainer.style.textAlign = 'right';
    }

    // اصلاح نمایش دکمه‌های ذخیره و تغییرات
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        submitRow.style.textAlign = 'left';
    }
}