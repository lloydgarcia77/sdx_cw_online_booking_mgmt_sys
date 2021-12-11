from django.urls import path
from booking import views

app_name = "booking"

urlpatterns = [
    path("", views.index_page, name="index_page"), 
    path("main-page/", views.main_page, name="main_page"), 
    path("profile/", views.profile, name="profile"), 

    # Users
    path("users/", views.users, name="users"), 
    path("users/add-user/", views.add_user, name="add_user"), 
    path("users/edit-user/<str:index>/", views.edit_user, name="edit_user"), 
    path("users/set-new-password-user/<str:index>/", views.set_new_password_users, name="set_new_password_users"), 
    path("users/delete-user/<str:index>/", views.delete_user, name="delete_user"), 

    # Staff
    path("staff/", views.staff, name="staff"),
    path("staff/add-staff/", views.add_staff, name="add_staff"), 
    path("staff/edit-staff/<str:index>/", views.edit_staff, name="edit_staff"), 
    path("staff/delete-staff/<str:index>/", views.delete_staff, name="delete_staff"), 

    # Inquiries
    path("inquiries/", views.inquiries, name="inquiries"), 
    path("inquiries/delete-inquiry/<str:index>/", views.delete_inquiries, name="delete_inquiries"), 

    # Services
    path("services/", views.services, name="services"), 
    path("services/create-service/", views.create_service, name="create_service"), 
    path("services/edit-service/<str:index>/", views.edit_service, name="edit_service"), 
    path("services/delete-service/<str:index>/", views.delete_service, name="delete_service"), 

    # Bookings 
    path("bookings/", views.bookings, name="bookings"), 
    path("bookings/view-client-booking-details/<str:index>/", views.view_client_booking_details, name="view_client_booking_details"), 
    path("bookings/reject-client-booking/<str:index>/", views.reject_client_booking, name="reject_client_booking"), 
    path("bookings/invoice-client-booking/<str:index>/", views.invoice_client_booking, name="invoice_client_booking"), 

    # Schedules
    path("schedules/", views.schedules, name="schedules"), 

    # Reports
    path("reports/", views.reports, name="reports"), 
    path("reports/view-invoice-client-booking-details/<str:index>/", views.view_invoice_client_booking_details, name="view_invoice_client_booking_details"), 
    path("reports/delete-invoice-client-booking/<str:index>/", views.delete_invoice_client_booking, name="delete_invoice_client_booking"), 
    path("reports/walkin-invoice-booking-add/", views.walkin_invoice_booking_add, name="walkin_invoice_booking_add"), 
    path("reports/walkin-invoice-booking-edit/<str:index>/", views.walkin_invoice_booking_edit, name="walkin_invoice_booking_edit"), 
    path("reports/walkin-invoice-booking-delete/<str:index>/", views.walkin_invoice_booking_delete, name="walkin_invoice_booking_delete"), 

    # Client Side 

    # My Bookings
    path("my-bookings/", views.my_bookings, name="my_bookings"), 
    path("my-bookings/set-schedule/<str:index>/", views.set_schedule, name="set_schedule"), 

    
    # My Bookings
    path("my-transactions/", views.my_transactions, name="my_transactions"), 
    path("my-transactions/view-booking-details/<str:index>/", views.view_booking_details, name="view_booking_details"), 
    path("my-transactions/delete-booking/<str:index>/", views.delete_booking, name="delete_booking"), 
]