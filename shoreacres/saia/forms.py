import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Classified, Events


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ("date", "title", "description", "img")

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['placeholder'] = 'Date (Required)'
        self.fields['title'].widget.attrs['placeholder'] = 'Title (Required)'
        self.fields['title'].widget.attrs['value'] = ''
        self.fields['description'].widget.attrs['placeholder'] = 'description (Required)'


class ClassifiedForm(forms.ModelForm):
    class Meta:
        model = Classified
        fields = ("title", "description", "img1", "img2", "img3")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "house_number", "street", "phone", "img")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name (Required)'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name (Required)'
        self.fields['house_number'].widget.attrs['placeholder'] = 'House Number'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone Number'

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
        if commit:
            p.save()
        return p


class EmailListForm(forms.Form):
    email = forms.EmailField(max_length=254)


class AuthForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username (Required)'
        self.fields['email'].widget.attrs['placeholder'] = 'Recovery Email (Required)'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password (Required)'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password (Required)'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email address already in use.')
        return email

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

