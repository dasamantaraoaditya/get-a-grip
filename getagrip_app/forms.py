from django.contrib.auth.models import User
from django import forms
from getagrip_app.models import *
from datetime import datetime


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': "text",
            'class': "form-control",
            'placeholder': "Username",
            'aria-describedby': "basic-addon1"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': "password",
            'class': "form-control",
            'placeholder': "Password",
            'aria-describedby': "basic-addon1"})
    )  # to make the password look like a * or . in password block
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'type': "email",
            'class': "form-control",
            'placeholder': "sample@mail.com",
            'aria-describedby': "basic-addon1"})
    )

    class Meta:  # meta data of the model
        model = User
        fields = ['username', 'password', 'email']


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': "text",
            'class': "form-control",
            'placeholder': "Task Title",
            'aria-describedby': "basic-addon1"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'type': "text",
            'class': "form-control",
            'placeholder': "Here goes the description regarding the task details . . . . .",
            'aria-describedby': "basic-addon1"})
    )  # to make the password look like a * or . in password block

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': "date",
            'class': "form-control",
            # "2017-06-06T22:22:55"
            'min': datetime.now().strftime("%Y-%m-%d"),
            'aria-describedby': "basic-addon1"})
    )

    # deadline = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={
    #         'type': "datetime-locale",
    #         'class': "form-control",
    #         # "2017-06-06T22:22:55"
    #         'min': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    #         'aria-describedby': "basic-addon1"})
    # )

    class Meta:
        model = tasks_log
        fields = ["title", "description", "deadline", "state", "type", "maintask"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['maintask'].queryset = tasks_log.objects.filter(createdBy=user)

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
            'type': "text",
            'class': "form-control",
            'placeholder': "UserName Or A PetName",
            'aria-describedby': "basic-addon1"})
    )
    contact_email = forms.CharField(required=True,
        widget=forms.EmailInput(attrs={
            'type': "email",
            'class': "form-control",
            'placeholder': "sample@mail.com",
            'aria-describedby': "basic-addon1"})
    )
    content = forms.CharField(required=True,
        widget=forms.Textarea(attrs={
            'type': "text",
            'class': "form-control",
            'placeholder': "Here goes the description regarding the Issue. . . . .",
            'aria-describedby': "basic-addon1"})
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label ="What do you want to say?"