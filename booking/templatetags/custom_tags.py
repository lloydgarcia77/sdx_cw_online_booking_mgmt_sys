from django import template
from booking import models
from django.utils import timezone 
import os, pytz, datetime

register = template.Library()

@register.filter
def custom_date_format(date):
    if date != None:      
        if isinstance(date, datetime.datetime):
            tz = pytz.timezone('Asia/Manila')
            date = timezone.localtime(date, tz)  
            date = date.strftime("%b. %d, %Y")  
            # date = date.strftime("%b. %d, %Y, %I:%M %p")  
    return date
@register.filter
def custom_time_format(time):
    if time != None:      
        
        time = time.strftime("%I:%M %p")   
    return time


@register.filter
def time(slot):
    time_slots = ['8:00am - 10:00am',
     '10:00am - 12:00pm',
     '12:00pm- 2:00pm',
     '2:00pm - 4:00pm',
     '4:00pm - 6:00pm',
     '6:00pm - 8:00pm']
    return time_slots[int(slot)-1]


@register.inclusion_tag("booking/load_services.html")
def show_services():    

    obj = models.ServicesModel.objects.all().distinct()

    return { 
        'obj': obj,
    }


@register.simple_tag
def get_user_count():
    users = models.User.objects.all().order_by("id").distinct().count() 
    return users

@register.simple_tag
def get_staff_count():
    o = models.Staff.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_inquiries_count():
    o = models.InquiriesModel.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_bookings_count():
    o = models.BookingModel.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_invoice_booking_count():
    o = models.InvoiceBookingModel.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_service_model_count():
    o = models.ServicesModel.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_walkin_invoice_count():
    o = models.WalkinInvoiceModel.objects.all().order_by("id").distinct().count() 
    return o

@register.simple_tag
def get_my_bookings_count(request):
    o = models.BookingModel.objects.all().filter(user=request.user).order_by("id").distinct().count() 
    return o
    
 