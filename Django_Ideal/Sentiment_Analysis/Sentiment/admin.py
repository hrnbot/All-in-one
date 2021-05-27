"""This File contains which model need to show in admin panel"""
from django.contrib import admin
from .models import User

admin.site.register(User)  #Registered User model to be shown in Admin Panel
