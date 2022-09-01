from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Todo, User


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
