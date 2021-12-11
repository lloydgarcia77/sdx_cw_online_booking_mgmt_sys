from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.conf import settings 
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
from .file_validators import file_validator_image, file_validator_valid_attachment 
from django.utils import timezone 
import os, pytz, datetime

# Create your models here.
class UserManager(BaseUserManager):
    """Manger for user profiles"""

    def create_user(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address, password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address, password=password)
        user.staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """Create and save a new superuser with the given details"""
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customized model for user in django"""
    GENDER_LIST = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    ROLE = (
        ('Administrator', 'Administrator'),
        ('Client', 'Client'), 
    ) 
    email = models.EmailField(max_length=50, unique=True)
    image = models.ImageField(upload_to="images/", blank=True, validators=[file_validator_image])
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    m_name = models.CharField(max_length=50, verbose_name="Middle Name")
    l_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender = models.CharField(max_length=50, choices=GENDER_LIST, default='Male')
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField()
    contact_no = models.CharField(max_length=11, verbose_name="Contact No", blank=True, null=True, unique=True) 
    role = models.CharField(max_length=50, choices=ROLE, default=ROLE[1][0])
    date_added = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name','m_name','l_name','age','gender', 'dob','contact_no', 'address',] # Email & Password are required by default.

    def get_encrpted_id(self):
        return settings.SIGNER.sign(self.id)

    def get_full_name(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'
    
    def get_short_name(self):
        return self.f_name
    
    def __str__(self):
        return self.email
      
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_absolute_url(self):
        return reverse("booking:edit_user", args=[settings.SIGNER.sign(self.id),])

    def get_absolute_url_set_new_password(self):
        return reverse("booking:set_new_password_users", args=[settings.SIGNER.sign(self.id),])

    def get_absolute_url_set_delete(self):
        return reverse("booking:delete_user", args=[settings.SIGNER.sign(self.id),])

    def save(self, *args, **kwargs): 
        # Invoking the functionality of save from parent class to be save to the database
        # Save the image first
        super(User, self).save(*args, **kwargs) 

        # [NOTE] https://www.codegrepper.com/code-examples/python/how+to+resize+an+image+with+pil
        # [NOTE] https://pillow.readthedocs.io/en/stable/releasenotes/2.7.0.html
        # The image is now ready for resizing after saving
        if self.image:
            # Access the image from the file path 
            file_image = Image.open(self.image.path) 

            # Getting the height and width and limiting it to 300
            if file_image.height > 350 or file_image.width > 350:
                # image resizing to 300x300 resolution
                image_resolution_output_size = (350, 350)
                # resing the image
                # file_image.thumbnail(image_resolution_output_size)
                resized_image = file_image.resize(image_resolution_output_size, Image.LANCZOS)
                # Saving the image
                resized_image.save(self.image.path) 


class Staff(models.Model):
    GENDER_LIST = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    image = models.ImageField(upload_to="staff_images/", blank=True, validators=[file_validator_image])
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    m_name = models.CharField(max_length=50, verbose_name="Middle Name")
    l_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender = models.CharField(max_length=50, choices=GENDER_LIST, default='Male')
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=100)
    address = models.TextField()
    contact_no = models.CharField(max_length=11, verbose_name="Contact No", blank=True, null=True, unique=True)  
    date_added = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'
     
    def __str__(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'
    
        
    def get_absolute_url(self):
        return reverse("booking:edit_staff", args=[settings.SIGNER.sign(self.id),])
 
    def get_absolute_url_delete(self):
        return reverse("booking:delete_staff", args=[settings.SIGNER.sign(self.id),])
      

class InquiriesModel(models.Model):
  
 
    f_name = models.CharField(max_length=100,)
    l_name = models.CharField(max_length=100,)
    subject = models.CharField(max_length=100,)
    message = models.TextField()
    email = models.EmailField(max_length=55,) 
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

 

    def __str__(self):
        return str(self.subject)
    
    # def get_absolute_url(self):
    #     return reverse("booking:view_booking_details", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_delete(self):
        return reverse("booking:delete_inquiries", args=[settings.SIGNER.sign(self.id),]) 
    

class ServicesModel(models.Model):

    VEHICLE_TYPE = (
        ('Motorcycle', 'Motorcycle'),
        ('Car', 'Car')
    )
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE, default="Motorcycle")
    price = models.IntegerField()
    desription = models.TextField()
    # duration = models.DurationField() 
    duration = models.CharField(max_length=100, blank=True, null=True) 
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicle_type":self.vehicle_type,
            "price":self.price,
            "desription":self.desription,
            "duration":self.duration,  
            "edit_url":self.get_absolute_url(),
            "delete_url":self.get_absolute_url_set_delete(),   
        }

    def get_absolute_url(self):
        return reverse("booking:edit_service", args=[settings.SIGNER.sign(self.id),]) 
 
    def get_absolute_url_set_delete(self):
        return reverse("booking:delete_service", args=[settings.SIGNER.sign(self.id),])

    def get_absolute_url_set_schedule(self):
        return reverse("booking:set_schedule", args=[settings.SIGNER.sign(self.id),])

    # Returns dict of all values


class BookingModel(models.Model):
    SLOT = (
        ('Slot 1', 'Slot 1'), 
        ('Slot 2', 'Slot 2'), 
        ('Slot 3', 'Slot 3'), 
    )
    TIME_SLOT = (
        ('1', '8:00am - 10:00am'),  
        ('2', '10:00am - 12:00pm'),  
        ('3', '12:00pm- 2:00pm'),  
        ('4', '2:00pm - 4:00pm'),  
        ('5', '4:00pm - 6:00pm'),  
        ('6', '6:00pm - 8:00pm'),  
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fk_bm_user")
    service = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, related_name="fk_bm_service") 
    date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT, default='Slot 1')
    time_slot = models.CharField(max_length=2, choices=TIME_SLOT, default='1')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'slot', 'time_slot'], 
                name='unique time slot'
            )
        ]
 

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse("booking:view_booking_details", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_delete(self):
        return reverse("booking:delete_booking", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_invoice(self):
        return reverse("booking:invoice_client_booking", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_view_full_details(self):
        return reverse("booking:view_client_booking_details", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_reject_booking(self):
        return reverse("booking:reject_client_booking", args=[settings.SIGNER.sign(self.id),]) 
    

class InvoiceBookingModel(models.Model):
    SLOT = (
        ('Slot 1', 'Slot 1'), 
        ('Slot 2', 'Slot 2'), 
        ('Slot 3', 'Slot 3'), 
    )
    TIME_SLOT = (
        ('1', '8:00am - 10:00am'),  
        ('2', '10:00am - 12:00pm'),  
        ('3', '12:00pm- 2:00pm'),  
        ('4', '2:00pm - 4:00pm'),  
        ('5', '4:00pm - 6:00pm'),  
        ('6', '6:00pm - 8:00pm'),  
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fk_ibm_user")
    service = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, related_name="fk_ibm_service") 
    date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT, default='Slot 1')
    time_slot = models.CharField(max_length=2, choices=TIME_SLOT, default='1')
    date_created = models.DateTimeField(auto_now_add=True) 
 

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse("booking:view_invoice_client_booking_details", args=[settings.SIGNER.sign(self.id),]) 
    
    def get_absolute_url_delete(self):
        return reverse("booking:delete_invoice_client_booking", args=[settings.SIGNER.sign(self.id),])  
    


class WalkinInvoiceModel(models.Model):
    SLOT = (
        ('Slot 1', 'Slot 1'), 
        ('Slot 2', 'Slot 2'), 
        ('Slot 3', 'Slot 3'), 
        ('Slot 4', 'Slot 4'), 
        ('Slot 5', 'Slot 5'), 
        ('Slot 6', 'Slot 6'), 
    )  
    name = models.CharField(max_length=100) 
    service = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, related_name="fk_wim_service") 
    date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT, default='Slot 1') 
    date_created = models.DateTimeField(auto_now_add=True) 
    
    def get_data(self):
        tz = pytz.timezone('Asia/Manila')
        # date = timezone.localtime(self.date, tz)
        date_created = timezone.localtime(self.date_created, tz)
        return {
            "id": self.id,
            "name": self.name, 
            "service":self.service.name,
            "date":self.date.strftime("%b. %d, %Y") ,
            "slot":self.slot,  
            "price":self.service.price,  
            "date_created":date_created.strftime("%b. %d, %Y") ,
            "edit_url":self.get_absolute_url(),
            "delete_url":self.get_absolute_url_delete(),   
        }

    def __str__(self):
        return str(self.name) 
    
    def get_absolute_url(self):
        return reverse("booking:walkin_invoice_booking_edit", args=[settings.SIGNER.sign(self.id),]) 
 
    def get_absolute_url_delete(self):
        return reverse("booking:walkin_invoice_booking_delete", args=[settings.SIGNER.sign(self.id),])
