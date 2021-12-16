from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q
from django.db.models import fields 
from booking import models
 
User = get_user_model()
 
 
class UserAdminCreationForms(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = '__all__'
    
    def clean(self):
        '''
            Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match!")
        
        return self.cleaned_data
    
    def save(self, commit=True):
        """
            Save the provided password in hashed format
        """
        
        # Invoke the super class save funtion to trigger the save method
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
        A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
    """

    password = ReadOnlyPasswordHashField()  

    class Meta:
        model = User
        fields = '__all__'
    
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

  
class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegistrationForm(forms.ModelForm): 

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

 
    # Apply predefined attributes of html element
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control secret-input',
                'placeholder': 'Full Address',
            }
        )
    )
    
    class Meta:
        model = User
        exclude = ('date_added', 'is_active', 'is_staff', 'is_superuser', 'role', 'password', 'groups', 'user_permissions', 'last_login')
        widgets = {'dob' : DateInput(format=('%Y-%m-%d'), attrs = {'class': 'form-control bg-light border-0 small', 'required': 'required'})}

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        """
            Apply predefined attributes of html element
        """
        self.fields['image'].widget.attrs = {  
            'accept': "image/*" ,
            'class': 'form-control bg-light border-0 small', 
            
        }

        self.fields['email'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'E-Mail',
            'required': 'required'
        }

        self.fields['f_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'First Name',
        }

        self.fields['m_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Middle Name',
        }

        self.fields['l_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Last Name',
        }

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'select2 form-control bg-light border-0 small', 
            'style': 'width: 100%',
            'placeholder': 'Gender',
        }

        self.fields['age'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Age', 
            'max': "120" 
        } 

        self.fields['contact_no'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Contact No',
            'required': 'required',
            'maxlength': "11"
        }
        self.fields['address'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Address', 
            'max': "120" 
        }  
        
        self.fields['password1'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Password',
        }

        self.fields['password2'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Confirm Password',
        }

    def clean_email(self):

        """
            Validates the integrity of email
        """

        email = self.cleaned_data.get('email') 
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("E-mail is already taken.")
        return email
    
    def clean_password2(self):
        """ 
        http://www.learningaboutelectronics.com/Articles/How-to-check-a-password-in-Django.php
        from django.contrib.auth.hashers import check_password 
        def changepassword(requests):

            currentpassword= request.user.password #user's current password

            form = ChangePasswordform(request.POST or None)

            if form.is_valid():
                currentpasswordentered= form.cleaned_data.get("lastpassword")
                password1= form.cleaned_data.get("newpassword1")
                password2= form.cleaned_data.get("newpassword2")

                matchcheck= check_password(currentpasswordentered, currentpassword)

            if matchcheck:
                #change password code
        """

        """
            Use Strict Password Validator
        """

        MIN_LEN = 8
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']

        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                   '*', '(', ')', '<', '!']

        WITH_DIGITS = False
        WITH_LCASE_CHARS = False
        WITH_UCASE_CHARS = False
        WITH_SYMBOLS = False
        WITH_REPEATABLE_CHARS = False

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
 


        if len(password1) < MIN_LEN and len(password2) < MIN_LEN:
            raise forms.ValidationError("Password is too short!")
        else:
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            else:
                for d in DIGITS:
                    if d in password2:
                        WITH_DIGITS = True
                        print("WITH DIGITS")
                        break
                        
                for lc in LOCASE_CHARACTERS:
                    if lc in password2:
                        WITH_LCASE_CHARS = True
                        print("WITH LCASE")
                        break
                for uc in UPCASE_CHARACTERS:
                    if uc in password2:
                        WITH_UCASE_CHARS = True
                        print("WITH UCASE")
                        break
                for s in SYMBOLS:
                    if s in password2:
                        WITH_SYMBOLS = True
                        print("WITH SYMBOLS")
                        break

                for c in range(len(password2)):
                    index = c + 1
                    if index < len(password2):
                        if password2[c] == password2[c+1]:
                            WITH_REPEATABLE_CHARS = True
                            print("WITH REPEATABLE CHARS")

                if not (WITH_DIGITS and WITH_SYMBOLS and WITH_UCASE_CHARS and WITH_LCASE_CHARS and not WITH_REPEATABLE_CHARS):
                    raise forms.ValidationError("Your password is too weak, please include characters with Uppercases, Lowercases, Special characters, and dont include repeated characters!") 

        return password2
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user



class UserProfileForm(forms.ModelForm): 
 
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control secret-input',
                'placeholder': 'Full Address',
            }
        )
    )
 

    class Meta:
        model = User
        exclude = ('email','date_added', 'is_active', 'is_staff', 'is_superuser', 'role', 'password', 'groups', 'user_permissions', 'last_login')
        widgets = {'dob' : DateInput(format=('%Y-%m-%d'), attrs = {'class': 'form-control bg-light border-0 small', 'required': 'required'})}


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['image'].widget.attrs = {  
            'accept': "image/*" ,
            'class': 'form-control bg-light border-0 small', 
        }
 
        self.fields['f_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'First Name',
        }

        self.fields['m_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Middle Name',
        }

        self.fields['l_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Last Name',
        }

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'select2 form-control bg-light border-0 small', 
            'style': 'width: 100%',
            'placeholder': 'Gender',
        }

        self.fields['age'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Age', 
            'max': "120" 
        } 

        self.fields['contact_no'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Contact No',
            'required': 'required',
            'maxlength': "11"
        }
        self.fields['address'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Address', 
            'max': "120" 
        }  


class UserEditForm(forms.ModelForm): 
 
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control secret-input',
                'placeholder': 'Full Address',
            }
        )
    )
 

    class Meta:
        model = User
        exclude = ('date_added', 'is_active', 'is_staff', 'is_superuser', 'role', 'password', 'groups', 'user_permissions', 'last_login')
        widgets = {'dob' : DateInput(format=('%Y-%m-%d'), attrs = {'class': 'form-control bg-light border-0 small', 'required': 'required'})}


    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'E-Mail',
        }

        self.fields['image'].widget.attrs = {  
            'accept': "image/*" ,
            'class': 'form-control bg-light border-0 small', 
        }
 
        self.fields['f_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'First Name',
        }

        self.fields['m_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Middle Name',
        }

        self.fields['l_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Last Name',
        }

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'select2 form-control bg-light border-0 small', 
            'style': 'width: 100%',
            'placeholder': 'Gender',
        }

        self.fields['age'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Age', 
            'max': "120" 
        } 

        self.fields['contact_no'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Contact No',
            'required': 'required',
            'maxlength': "11"
        }
        self.fields['address'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Address', 
            'max': "120" 
        }  


class StaffForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-control secret-input',
                'placeholder': 'Full Address',
            }
        )
    )
  
    class Meta:
        model = models.Staff
        exclude = ('date_added', 'id')
        widgets = {'dob' : DateInput(format=('%Y-%m-%d'), attrs = {'class': 'form-control bg-light border-0 small', 'required': 'required'})}


    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
 

        self.fields['image'].widget.attrs = {  
            'accept': "image/*" ,
            'class': 'form-control bg-light border-0 small', 
        }
 
        self.fields['f_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'First Name',
        }

        self.fields['m_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Middle Name',
        }

        self.fields['l_name'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Last Name',
        }

        self.fields['gender'].widget.attrs = {
            'type': 'text',
            'class': 'select2 form-control bg-light border-0 small', 
            'style': 'width: 100%',
            'placeholder': 'Gender',
        }

        self.fields['age'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Age', 
            'max': "120" 
        } 

        self.fields['contact_no'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Contact No',
            'required': 'required',
            'maxlength': "11"
        }

        self.fields['position'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Position',
            'required': 'required', 
        }

        self.fields['address'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Address', 
            'max': "120" 
        }  
 

class InquiriesForm(forms.ModelForm):

    class Meta:
        model = models.InquiriesModel
        exclude = ('date_created','id', 'date_updated')

    def __init__(self, *args, **kwargs):
        super(InquiriesForm, self).__init__(*args, **kwargs) 

        self.fields['f_name'].widget.attrs = {  
            'placeholder': 'First Name',
            'required': 'required',
        }
        self.fields['l_name'].widget.attrs = {  
            'placeholder': 'Last Name',
            'required': 'required',
        }
        self.fields['subject'].widget.attrs = {  
            'placeholder': 'Subject',
            'required': 'required',
        }
        self.fields['email'].widget.attrs = {  
            'placeholder': 'Email',
            'required': 'required',
        }
        self.fields['message'].widget.attrs = {  
            'placeholder': 'Message',
            'required': 'required',
        } 


class UserSetNewPassword(forms.ModelForm): 

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
 
    
    class Meta:
        model = User 
        fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSetNewPassword, self).__init__(*args, **kwargs) 
        self.fields['password1'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Password',
        }

        self.fields['password2'].widget.attrs = {
            'type': 'text',
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Confirm Password',
        }
 
    
    def clean_password2(self):
        """ 
        http://www.learningaboutelectronics.com/Articles/How-to-check-a-password-in-Django.php
        from django.contrib.auth.hashers import check_password 
        def changepassword(requests):

            currentpassword= request.user.password #user's current password

            form = ChangePasswordform(request.POST or None)

            if form.is_valid():
                currentpasswordentered= form.cleaned_data.get("lastpassword")
                password1= form.cleaned_data.get("newpassword1")
                password2= form.cleaned_data.get("newpassword2")

                matchcheck= check_password(currentpasswordentered, currentpassword)

            if matchcheck:
                #change password code
        """

        """
            Use Strict Password Validator
        """

        MIN_LEN = 8
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']

        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                   '*', '(', ')', '<', '!']

        WITH_DIGITS = False
        WITH_LCASE_CHARS = False
        WITH_UCASE_CHARS = False
        WITH_SYMBOLS = False
        WITH_REPEATABLE_CHARS = False

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
 


        if len(password1) < MIN_LEN and len(password2) < MIN_LEN:
            raise forms.ValidationError("Password is too short!")
        else:
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            else:
                for d in DIGITS:
                    if d in password2:
                        WITH_DIGITS = True
                        print("WITH DIGITS")
                        break
                        
                for lc in LOCASE_CHARACTERS:
                    if lc in password2:
                        WITH_LCASE_CHARS = True
                        print("WITH LCASE")
                        break
                for uc in UPCASE_CHARACTERS:
                    if uc in password2:
                        WITH_UCASE_CHARS = True
                        print("WITH UCASE")
                        break
                for s in SYMBOLS:
                    if s in password2:
                        WITH_SYMBOLS = True
                        print("WITH SYMBOLS")
                        break

                for c in range(len(password2)):
                    index = c + 1
                    if index < len(password2):
                        if password2[c] == password2[c+1]:
                            WITH_REPEATABLE_CHARS = True
                            print("WITH REPEATABLE CHARS")

                if not (WITH_DIGITS and WITH_SYMBOLS and WITH_UCASE_CHARS and WITH_LCASE_CHARS and not WITH_REPEATABLE_CHARS):
                    raise forms.ValidationError("Your password is too weak, please include characters with Uppercases, Lowercases, Special characters, and dont include repeated characters!") 

        return password2
    

    def save(self, commit=True):
        user = super(UserSetNewPassword, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class ServicesForm(forms.ModelForm):

    class Meta:
        model = models.ServicesModel
        exclude = ('date_created','id', 'date_updated')

    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs) 

        self.fields['name'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Name',
        }
        self.fields['vehicle_type'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Vehicle Type',
        }
        self.fields['price'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Price',
        }
        self.fields['desription'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Description',
        }
        self.fields['duration'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Duration',
        }


class WalkinInvoiceForm(forms.ModelForm):

  
    class Meta:
        model = models.WalkinInvoiceModel
        exclude = ('date_created','id')
        widgets = {
            'date' : DateInput(format=('%Y-%m-%d'), attrs = {'class': 'form-control bg-light border-0 small', 'required': 'required'}),
            # 'time_from' : forms.TimeInput(format='%I:%M %p', attrs={'type': 'time', 'class': 'form-control bg-light border-0 small', 'required': 'required'}),
            # 'time_to' : forms.TimeInput(format='%I:%M %p', attrs={'type': 'time', 'class': 'form-control bg-light border-0 small', 'required': 'required'}),
            'time_from' : forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control bg-light border-0 small', 'required': 'required'}),
            'time_to' : forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control bg-light border-0 small', 'required': 'required'}),
            }
        
        # time_from = forms.TimeField( 
        #     widget=forms.TimeInput(
        #         format='%I:%M', attrs={'type': 'time'}
        #     ),
        #     input_formats=('%I:%M',),
        #     required=True,
        # )
        # time_to = forms.TimeField( 
        #     widget=forms.TimeInput(
        #         format='%I:%M', attrs={'type': 'time'}
        #     ),
        #     input_formats=('%I:%M',),
        #     required=True,
        # )

    def __init__(self, *args, **kwargs):
        super(WalkinInvoiceForm, self).__init__(*args, **kwargs) 

        self.fields['name'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small', 
            'placeholder': 'Client Name / Car Model, Brand',
            'required': 'required',
        }
        
        self.fields['service'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small',  
            'required': 'required',
        } 
        # self.fields['time_from'].widget.attrs = { 
        #     'type' : 'time',
        #     'min' : '09:00',
        #     'max' : '18:00',
        #     'class': 'form-control bg-light border-0 small',   
        #     'required': 'required',
        # } 
        # self.fields['time_to'].widget.attrs = { 
        #     'type' : 'time',
        #     'min' : '09:00',
        #     'max' : '18:00',
        #     'class': 'form-control bg-light border-0 small',  
        #     'required': 'required',
        # } 

        self.fields['slot'].widget.attrs = { 
            'class': 'form-control bg-light border-0 small',  
            'required': 'required',
        } 






