from django.db.models.query_utils import PathInfo
from django.shortcuts import render, get_object_or_404
from django.http import (
    JsonResponse,
    Http404,
    HttpResponseRedirect
)
from django.core.signing import Signer
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.files import File
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from functools import reduce
from booking import (
    models,
    forms, 
)
import json, os, pytz, operator

# Decorator
def roles(**user_type):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            user = get_object_or_404(models.User, email=request.user.email)   
            if request.user.is_active: 
                
                utype  = user_type.get("type", False)    
                
                if utype == user.role:
                    kwargs['user'] = user
                    return view_method(request, *args, **kwargs)
                else: 
                    raise Http404() 
                    
            else:
                raise Http404()
        return _arguments_wrapper
    return _method_wrapper


# Error pages 
def error_404(request, exception):
    return render(request, "error/error_404.html", {})


def error_500(request):
    return render(request, "error/error_500.html", {})


# Create your views here.
def index_page(request, *args, **kwargs):
    template_name = "booking/index.html" 
    if request.method == 'GET':
        form = forms.InquiriesForm(request.GET or None)
    elif request.method == 'POST':
       
        form = forms.InquiriesForm(request.POST or None) 
        if form.is_valid():
            form.save()
            print("SADD")
            return HttpResponseRedirect(reverse("inquiry-success"))
        else:
            print(form.errors)
    context = { 
        'form': form,
    }
    return render(request, template_name, context)


def login_page(request):
    template_name = "registration/login.html"

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # request.session.set_expiry(request.session.get_expiry_age())
                previous_page = request.GET.get('next', reverse("booking:main_page"))
                return HttpResponseRedirect(previous_page)
            else:
                messages.error(request, "Your account is needs approval, Please contact your administrator!")
        else:
            messages.error(request, "Your account is INVALID!")
        
    return render(request, template_name)


def registration_page(request):
    template_name = "registration/register.html"
    if request.method == 'GET':
        form = forms.UserRegistrationForm(request.GET or None) 
    elif request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST or None, request.FILES) 
        if form.is_valid():
            userRegForm = form.save(commit=False)
            userRegForm.is_active = False
            userRegForm.is_staff = False
            userRegForm.is_superuser = False
            userRegForm.save()
            messages.success(request, "Your account was successfully created!")
            return HttpResponseRedirect(reverse("login")) 

    context = {
        'form': form,
    }

    return render(request, template_name, context)


@login_required
def main_page(request, *args, **kwargs):
    template_name = "booking/main_page.html"
    # user = kwargs['user']

    context = {
        'user': 'user',
    }
    return render(request, template_name, context)


@login_required
def profile(request):
    template_name = "booking/profile.html"

    user = get_object_or_404(models.User, email=request.user.email)
    if request.method == 'GET':
        form = forms.UserProfileForm(request.GET or None, instance=user) 
    elif request.method == 'POST':
        form = forms.UserProfileForm(request.POST or None, request.FILES, instance=user) 
        if form.is_valid():
            form = form.save(commit=False) 
            form.save()
            messages.success(request, "Your account was successfully Updated!")
            return HttpResponseRedirect(reverse("booking:main_page")) 

    context = {
        'form': form,
    }

    return render(request, template_name, context)

# User Management
@login_required
@roles(type='Administrator')
def users(request, *args, **kwargs):
    template_name = "booking/users/users.html"
    user = kwargs['user'] 
    users_list = models.User.objects.all().order_by('-id').distinct()

    context = { 
        'users': users_list,
    }

    return render(request, template_name, context)


@login_required
@roles(type='Administrator')
def add_user(request, *args, **kwargs):
    template_name = "booking/users/add_user.html"
    user = kwargs['user'] 
    
    if request.method == 'GET':
        form = forms.UserRegistrationForm(request.GET or None) 
    elif request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST or None, request.FILES) 
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.is_active = True
            user_form.is_staff = True
            user_form.is_superuser = False
            user_form.role = 'Administrator'
            user_form.save()
            messages.success(request, "New account was successfully created!")
            return HttpResponseRedirect(reverse("booking:users")) 

    context = {
        'form': form,
    }
 

    return render(request, template_name, context)



@login_required
@roles(type='Administrator')
def edit_user(request, *args, **kwargs):
    template_name = "booking/users/edit_user.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.User, id=settings.SIGNER.unsign(index), role='Administrator')
    
    if request.method == 'GET':
        form = forms.UserEditForm(request.GET or None, instance=obj) 
    elif request.method == 'POST':
        form = forms.UserEditForm(request.POST or None, request.FILES, instance=obj) 
        if form.is_valid():
            form = form.save(commit=False) 
            form.save()
            messages.success(request, "Account has successfully updated!")
            return HttpResponseRedirect(reverse("booking:users")) 

    context = {
        'form': form,
        'user': user,
        'obj': obj,
    }
 

    return render(request, template_name, context)
 


@login_required
@roles(type='Administrator')
def set_new_password_users(request, *args, **kwargs): 
    data = dict()
    template_name = "booking/users/set_new_password.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.User, id=settings.SIGNER.unsign(index), role='Administrator')
 
    if request.is_ajax(): 
        if request.method == 'GET':
            form = forms.UserSetNewPassword(request.GET or None, instance=obj)
        elif request.method == 'POST':
            form = forms.UserSetNewPassword(request.POST or None, instance=obj)
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.save()   
                data['form_is_valid'] = True       

        context = {
            'user': user,
            'form': form, 
            'obj': obj,
        }
        data['html_form'] = render_to_string(template_name, context, request)
        return JsonResponse(data)        
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def delete_user(request, *args, **kwargs):
    data = dict()
    template_name = "booking/users/delete_user.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.User, id=settings.SIGNER.unsign(index), role='Administrator') 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()


# Staff
@login_required
@roles(type='Administrator')
def staff(request, *args, **kwargs):
    template_name = "booking/staff/staff.html"
    user = kwargs['user']  
    staff_list = models.Staff.objects.all().order_by('-id').distinct()
    context = {  
        'user': user,
        'staffs': staff_list,
    }

    return render(request, template_name, context)


@login_required
@roles(type='Administrator')
def add_staff(request, *args, **kwargs):
    template_name = "booking/staff/add_staff.html"
    user = kwargs['user'] 
    
    if request.method == 'GET':
        form = forms.StaffForm(request.GET or None) 
    elif request.method == 'POST':
        form = forms.StaffForm(request.POST or None, request.FILES) 
        if form.is_valid():
            form = form.save(commit=False) 
            form.save()
            messages.success(request, "New staff has been successfully created!")
            return HttpResponseRedirect(reverse("booking:staff")) 

    context = {
        'form': form,
    }
 

    return render(request, template_name, context)


@login_required
@roles(type='Administrator')
def edit_staff(request, *args, **kwargs):
    template_name = "booking/staff/edit_staff.html"
    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.Staff, id=settings.SIGNER.unsign(index))
    
    if request.method == 'GET':
        form = forms.StaffForm(request.GET or None, instance=obj) 
    elif request.method == 'POST':
        form = forms.StaffForm(request.POST or None, request.FILES, instance=obj) 
        if form.is_valid():
            form = form.save(commit=False) 
            form.save()
            messages.success(request, "Staff has been successfully updated!")
            return HttpResponseRedirect(reverse("booking:staff")) 

    context = {
        'form': form,
        'user': user,
        'obj': obj,
    }
 

    return render(request, template_name, context)
 

@login_required
@roles(type='Administrator')
def delete_staff(request, *args, **kwargs):
    data = dict()
    template_name = "booking/staff/delete_staff.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.Staff, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()

 
# Inquiries
@login_required
@roles(type='Administrator')
def inquiries(request, *args, **kwargs):
    template_name = "booking/inquiries/inquiries.html"
    user = kwargs['user']  
    inquiries = models.InquiriesModel.objects.all().order_by('-id').distinct()

    context = { 
        'user': user,
        'inquiries': inquiries,
    }
 

    return render(request, template_name, context)


@login_required
@roles(type='Administrator')
def delete_inquiries(request, *args, **kwargs):
    data = dict()
    template_name = "booking/inquiries/delete_inquiries.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.InquiriesModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()

 
# Services
@login_required
@roles(type='Administrator')
def services(request, *args, **kwargs):
    template_name = "booking/services/services.html"
    user = kwargs['user'] 
    objs = models.ServicesModel.objects.all().order_by('-id').distinct()

    context = { 
        'user': user,
        'objs': objs,
    }

    return render(request, template_name, context)


@login_required
@roles(type='Administrator')
def create_service(request, *args, **kwargs):
    data = dict()
    template_name = "booking/services/create_services.html"

    user = kwargs['user'] 

    if request.is_ajax():
        if request.method == 'GET':
            form = forms.ServicesForm(request.GET or None)
        elif request.method == 'POST':
            form = forms.ServicesForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.save()   
                data['object_data'] = instance.get_data()
                data['form_is_valid'] = True
            
        context = {
            'user': user,
            'form': form,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def edit_service(request, *args, **kwargs):
    data = dict()
    template_name = "booking/services/edit_services.html"

    user = kwargs['user'] 
    index = kwargs['index']

    obj = get_object_or_404(models.ServicesModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax():
        if request.method == 'GET':
            form = forms.ServicesForm(request.GET or None, instance=obj)
        elif request.method == 'POST':
            form = forms.ServicesForm(request.POST or None, instance=obj)
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.save()   
                data['object_data'] = instance.get_data()
                data['form_is_valid'] = True
            
        context = {
            'user': user,
            'form': form,
            'obj': obj,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def delete_service(request, *args, **kwargs):
    data = dict()
    template_name = "booking/services/delete_services.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.ServicesModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()


# Bookings
@login_required
@roles(type='Administrator')
def bookings(request, *args, **kwargs):
    template_name = "booking/bookings/bookings.html"
    user = kwargs['user']  
    bookings = models.BookingModel.objects.all().order_by('-id').distinct()

    context = { 
        'user': user,
        'bookings': bookings,
    }
 

    return render(request, template_name, context)

 
@login_required
@roles(type='Administrator')
def view_client_booking_details(request, *args, **kwargs):
    data = dict()
    template_name = "booking/bookings/view_client_booking_details.html"

    user = kwargs['user'] 
    index = kwargs['index']

    obj = get_object_or_404(models.BookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax():
        if request.method == 'GET':
            pass
        context = {
            'user': user, 
            'obj': obj,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def reject_client_booking(request, *args, **kwargs):
    data = dict()
    template_name = "booking/bookings/reject_client_booking.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.BookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def invoice_client_booking(request, *args, **kwargs):
    data = dict()
    template_name = "booking/bookings/invoice_booking.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.BookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            invoice = models.InvoiceBookingModel(
                user=obj.user,
                service=obj.service,
                date=obj.date,
                slot=obj.slot,
                time_slot=obj.time_slot,
            )
            invoice.save()
            
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()

 
# Schedules
@login_required
@roles(type='Administrator')
def schedules(request, *args, **kwargs):
    template_name = "booking/schedule/schedule.html"
    user = kwargs['user']   

    def get_available_slot(slot):
        TIME_SLOTS = [1,2,3,4,5,6]
        return  list(set(TIME_SLOTS) - set([int(x.time_slot) for x in slot]))
    if request.is_ajax():
        data = dict()
        if request.method == 'GET':
            date = request.GET.get('date','None') 
            schedules = models.BookingModel.objects.all().filter(date=date)
            s1_book = schedules.filter(slot='Slot 1')
            s2_book = schedules.filter(slot='Slot 2')
            s3_book = schedules.filter(slot='Slot 3')
       
             
            data['date'] = date
            data['slot1'] =  get_available_slot(s1_book) 
            data['slot2'] =  get_available_slot(s2_book) 
            data['slot3'] =  get_available_slot(s3_book) 
            return JsonResponse(data)
    context = { 
        'user': user, 
    }
 

    return render(request, template_name, context)


# Reports
@login_required
@roles(type='Administrator')
def reports(request, *args, **kwargs):
    template_name = "booking/reports/reports.html"
    user = kwargs['user']   

    invoice_booking = models.InvoiceBookingModel.objects.all().order_by('-id').distinct()
    invoice_walkin = models.WalkinInvoiceModel.objects.all().order_by('-id').distinct()

    context = {  
        'user': user, 
        'invoice_booking':invoice_booking,
        'invoice_walkin':invoice_walkin,
    }

    return render(request, template_name, context)

@login_required
@roles(type='Administrator')
def view_invoice_client_booking_details(request, *args, **kwargs):
    data = dict() 
    template_name = "booking/reports/view_invoice_client_booking_details.html"

    user = kwargs['user'] 
    index = kwargs['index']

    obj = get_object_or_404(models.InvoiceBookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax():
        if request.method == 'GET':
            pass
        context = {
            'user': user, 
            'obj': obj,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def delete_invoice_client_booking(request, *args, **kwargs):
    data = dict()
    template_name = "booking/reports/delete_invoice_client_booking.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.InvoiceBookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def walkin_invoice_booking_add(request, *args, **kwargs):
    data = dict()
    template_name = "booking/reports/walkin_invoice_booking_add.html"

    user = kwargs['user'] 

    if request.is_ajax():
        if request.method == 'GET':
            form = forms.WalkinInvoiceForm(request.GET or None)
        elif request.method == 'POST':
            form = forms.WalkinInvoiceForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.save()    
                data['object_data'] = instance.get_data()
                data['form_is_valid'] = True
            
        context = {
            'user': user,
            'form': form,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def walkin_invoice_booking_edit(request, *args, **kwargs):
    data = dict()
    template_name = "booking/reports/walkin_invoice_booking_edit.html"

    user = kwargs['user'] 
    index = kwargs['index']

    obj = get_object_or_404(models.WalkinInvoiceModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax():
        if request.method == 'GET':
            form = forms.WalkinInvoiceForm(request.GET or None, instance=obj)
        elif request.method == 'POST':
            form = forms.WalkinInvoiceForm(request.POST or None, instance=obj)
            if form.is_valid():
                instance = form.save(commit=False) 
                instance.save()   
                data['object_data'] = instance.get_data()
                data['form_is_valid'] = True
            
        context = {
            'user': user,
            'form': form,
            'obj': obj,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Administrator')
def walkin_invoice_booking_delete(request, *args, **kwargs):
    data = dict()
    template_name = "booking/reports/walkin_invoice_booking_delete.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.WalkinInvoiceModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()




# ========================[Client Side]=============================

@login_required
@roles(type='Client')
def my_bookings(request, *args, **kwargs):
    template_name = "booking/client/my_bookings/my_bookings.html"
    user = kwargs['user']  
    objs = models.ServicesModel.objects.all().order_by('-id').distinct()

    context = { 
        'user': user,
        'objs': objs,
    }
 

    return render(request, template_name, context)

 
@login_required
@roles(type='Client')
def set_schedule(request, *args, **kwargs):
    template_name = "booking/client/my_bookings/set_schedule.html"
    user = kwargs['user']   
    index = kwargs['index']   
    obj = get_object_or_404(models.ServicesModel, id=settings.SIGNER.unsign(index)) 

    SLOTS = 18
    TIME_SLOTS = [1,2,3,4,5,6]
    schedule_data = dict()
    fully_booked_dates = []
    schedule_list = []
    
    def get_available_slot(slot):
        return  list(set(TIME_SLOTS) - set([int(x.time_slot) for x in slot]))
     

    for day in range(7):  
        temp_dict = dict()
        day = datetime.today() + timedelta(days=day) 
        #z = datetime.today() + timedelta(days=7) 
        # print(z.strftime("%Y-%m-%d")) 
        # bookings = models.BookingModel.objects.all().filter(date__range=[datetime.today(), z]) 
        bookings = models.BookingModel.objects.all().filter(date=day)

        if bookings.count() == SLOTS:
            fully_booked_dates.append(str(day.strftime("%Y-%m-%d")))

        s1_book = bookings.filter(slot='Slot 1')
        s2_book = bookings.filter(slot='Slot 2')
        s3_book = bookings.filter(slot='Slot 3')
         

        temp_dict['date'] = str(day.strftime("%Y-%m-%d"))
        temp_dict['available_slots_slot1'] = get_available_slot(s1_book)
        temp_dict['available_slots_slot2'] = get_available_slot(s2_book)
        temp_dict['available_slots_slot3'] = get_available_slot(s3_book)

        schedule_list.append(temp_dict)

    

    schedule_data['fully_booked_dates'] = fully_booked_dates
    schedule_data['schedule_list'] = schedule_list


    # print(json.dumps(schedule_data, sort_keys=True, indent=4))

    if request.is_ajax():
        data = dict()

        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            # Do post JSON string like this. 
            # data: {'data': JSON.stringify({'fruit': selected})} 
            # and receive like 
            # data = json.loads(request.POST.get('data', ''))
            data = json.loads(request.POST.get('data', ''))
            book = models.BookingModel.objects.create(user=user, service=obj, date=data['date'], slot=data['slot'], time_slot=data['time'])
            book.save() 
            data['form_is_valid'] = True
            messages.success(request, "Your booking has been successfully done and scheduled!")

        context = {
            'user': user,
            'obj': obj,
        }

        data['html_form'] = render_to_string('booking/client/my_bookings/booking_confirmation.html', context, request) 
        return JsonResponse(data)

 
    context = { 
        'user': user, 
        'obj': obj,
        'schedule_data': json.dumps(schedule_data),
    }
 

    return render(request, template_name, context)


@login_required
@roles(type='Client')
def my_transactions(request, *args, **kwargs):
    template_name = "booking/client/my_transactions/my_transactions.html"
    user = kwargs['user']   
    bookings = models.BookingModel.objects.all().filter(user=user).order_by('-id').distinct()
     
    context = { 
        'user': user, 
        'bookings': bookings,
    }
 

    return render(request, template_name, context)



@login_required
@roles(type='Client')
def view_booking_details(request, *args, **kwargs):
    data = dict()
    template_name = "booking/client/my_transactions/view_details.html"

    user = kwargs['user'] 
    index = kwargs['index']

    obj = get_object_or_404(models.BookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax():
        if request.method == 'GET':
            pass
        context = {
            'user': user, 
            'obj': obj,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()


@login_required
@roles(type='Client')
def delete_booking(request, *args, **kwargs):
    data = dict()
    template_name = "booking/client/my_transactions/delete_booking.html"

    user = kwargs['user'] 
    index = kwargs['index'] 

    obj = get_object_or_404(models.BookingModel, id=settings.SIGNER.unsign(index)) 
		
    if request.is_ajax(): 
        if request.method == 'GET':
            context = {
                'user': user,
                'obj': obj,        
            }
            data['html_form'] = render_to_string(template_name, context, request) 

        elif request.method == 'POST':
            obj.delete()
            data['form_is_valid'] = True
        
        return JsonResponse(data)         
    else:
        raise Http404()


