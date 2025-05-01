// RTL support for Django Unfold Admin

document.addEventListener('DOMContentLoaded', function() {
    // Check if page is in RTL mode
    const isRTL = document.documentElement.dir === 'rtl';

    if (isRTL) {
        // Fix any JavaScript-based components that need RTL handling

        // Fix date picker popup positioning
        const dateInputs = document.querySelectorAll('.unfold-datetime input');
        dateInputs.forEach(input => {
            input.addEventListener('click', function(e) {
                setTimeout(() => {
                    const calendar = document.querySelector('.calendar');
                    if (calendar) {
                        calendar.style.right = 'auto';
                        const rect = input.getBoundingClientRect();
                        calendar.style.left = rect.left + 'px';
                    }
                }, 100);
            });
        });

        // Fix filter dropdowns
        const filterButtons = document.querySelectorAll('.unfold-filters-button');
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                setTimeout(() => {
                    const dropdown = document.querySelector('.unfold-filters-dropdown');
                    if (dropdown) {
                        dropdown.style.left = 'auto';
                        dropdown.style.right = '0';
                    }
                }, 100);
            });
        });

        // Fix any Select2 dropdowns if they're being used
        if (window.jQuery && window.jQuery.fn.select2) {
            window.jQuery('.unfold-select select').on('select2:open', function() {
                setTimeout(() => {
                    const dropdown = document.querySelector('.select2-dropdown');
                    if (dropdown) {
                        const select = window.jQuery(this);
                        const rect = select[0].getBoundingClientRect();
                        dropdown.style.left = 'auto';
                        dropdown.style.right = (window.innerWidth - rect.right) + 'px';
                    }
                }, 100);
            });
        }
    }
});