from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForms, UserAdminChangeForm
from booking import models

admin.site.site_header = 'Super Administrator'
admin.site.index_title = 'Super Administrator Page'
admin.site.site_title = 'Super Administrator Panel'


User = get_user_model()

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # the forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForms

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'is_staff','is_active', 'is_superuser']
    list_filter = ['is_staff']

    fieldsets = (
        ("Account", {
            'fields': 
                (
                    'email', 
                    'password',
                )
        }), 
        ('Personal Info', {'fields': (
            'image',
            'f_name',
            'm_name',
            'l_name',
            'gender',
            'dob',
            'age',
            'address',
            'contact_no',
            'role'
        )}),
        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser'
                )
            }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    
    add_fieldsets = (
       
         ('Personal Info', {'fields': (
            'image',
            'f_name',
            'm_name',
            'l_name',
            'gender',
            'dob',
            'age',
            'address',
            'contact_no',
            'role'
        )}),
        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser'
                )
        }),
        (
            "Account", {
                'classes': ('wide', ),
                'fields': ('email', 'password', 'password_2')
            }
        ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

class StaffAdmin(ImportExportModelAdmin):
    list_display = ('id', 'f_name', 'm_name', 'l_name', 'gender', 'dob', 'age', 'position','address','contact_no', 'date_added')
    list_editable = ('f_name', 'm_name', 'l_name', 'gender', 'dob', 'age', 'position','address','contact_no', )
    list_filter = ('gender',)
    search_fields = ('id', 'f_name', 'm_name', 'l_name', 'gender', 'address', 'contact_no')  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.Staff, StaffAdmin)

class InquiriesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'f_name', 'l_name', 'subject', 'message', 'email', 'date_updated', 'date_created')
    list_editable = ('f_name', 'l_name', 'subject', 'message', 'email', )
    list_filter = ()
    search_fields = ('id', 'f_name', 'l_name', 'subject', 'message', 'email', )  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.InquiriesModel, InquiriesAdmin)

class ServicesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'vehicle_type', 'price', 'desription', 'duration', 'date_updated', 'date_created')
    list_editable = ('name', 'vehicle_type', 'price', 'desription', 'duration')
    list_filter = ('vehicle_type',)
    search_fields = ('id', 'name', 'vehicle_type','price', 'desription', 'duration', )  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.ServicesModel, ServicesAdmin)


class BookingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'service', 'date', 'slot', 'time_slot', 'date_updated', 'date_created')
    list_editable = ('user', 'service', 'date', 'slot', 'time_slot',)
    list_filter = ('service', 'slot', 'date')
    search_fields = ('id', 'date', 'slot', 'time_slot',)  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.BookingModel, BookingAdmin)

class InvoiceBookingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'service', 'date', 'slot', 'time_slot', 'date_created')
    list_editable = ('user', 'service', 'date', 'slot', 'time_slot',)
    list_filter = ('service', 'slot', 'date')
    search_fields = ('id', 'date', 'slot', 'time_slot',)  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.InvoiceBookingModel, InvoiceBookingAdmin)

class WalkinInvoiceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'service', 'date', 'time_from', 'time_to', 'slot',  'date_created')
    list_editable = ('service', 'time_from', 'time_to', 'slot',)
    list_filter = ('service', 'slot', 'date')
    search_fields = ('id', 'date', 'slot',)  
    ordering = ['id',]
    list_per_page = 10

admin.site.register(models.WalkinInvoiceModel, WalkinInvoiceAdmin)