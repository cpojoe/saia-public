from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile, Classified
import re
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.forms.widgets import FileInput


class ClassifiedForm(forms.ModelForm):
    class Meta:
        model = Classified
        fields = ("title", "description", "img1", "img2", "img3")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "house_number", "street", "phone", "img")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name (Required)'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name (Required)'
        self.fields['email'].widget.attrs['placeholder'] = 'Email (Required)'
        self.fields['house_number'].widget.attrs['placeholder'] = 'House Number'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'This email address is already registered.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) > 0:
            phone = phone.replace('-', '').replace(' ', '').replace('.', '').replace('(', '').replace(')', '')
            if len(phone) != 10:
                raise forms.ValidationError(u'Phone number entered incorrectly.')
            if not phone.isdigit():
                raise forms.ValidationError(u'Phone number contains illegal characters.')
            phone = '(' + phone[:3] + ')' + ' ' + phone[3:6] + '-' + phone[6:10]
        return phone


    def save(self, commit=True):
        p = super(ProfileForm, self).save(commit=False)
        if self.cleaned_data['first_name']:
            p.first_name = self.cleaned_data['first_name'].title()
        if self.cleaned_data['last_name']:
            p.last_name = self.cleaned_data['last_name'].title()
        if self.cleaned_data['street']:
            p.street = self.cleaned_data['street'].title()
        p.email = self.cleaned_data["email"]
        print self.cleaned_data['img']
        if commit:
            p.save()
        return p

class EmailListForm(forms.Form):
    email = forms.EmailField(max_length=254)

class AuthForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'