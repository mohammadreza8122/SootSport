# -*- coding: utf-8 -*-
from django import forms
from .models import TimeSlot, Discount


class TimeSlotAdminForm(forms.ModelForm):
    """فرم مدیریت سانس‌ها با پشتیبانی از تاریخ جلالی"""
    
    class Meta:
        model = TimeSlot
        fields = ('facility', 'date', 'start_time', 'end_time', 'base_price', 'discount', 'is_available', 'gender_type')


class DiscountAdminForm(forms.ModelForm):
    """فرم مدیریت تخفیف‌ها با پشتیبانی از تاریخ جلالی"""
    
    class Meta:
        model = Discount
        fields = ('code', 'description', 'discount_type', 'value', 'max_discount_amount', 
                  'start_date', 'end_date', 'usage_limit', 'is_active') 