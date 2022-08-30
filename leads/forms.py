from dataclasses import fields
from pyexpat import model
from urllib import request
from django import forms
from .models import Agent, Category, Lead
from django.contrib.auth.forms import (UserCreationForm,UsernameField)
from django.contrib.auth import get_user_model

class LeadForm(forms.ModelForm):
    
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )


class CustomUserCreationForm(UserCreationForm):
   class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}
        
        
class AssignAgentForm(forms.Form):
    agent=forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self,*args, **kwargs):
        request=kwargs.pop('request')
        agents=Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args, **kwargs)
        self.fields['agent'].queryset=agents
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=(
            'name',
        )
        
class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields=('category',)