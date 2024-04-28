from django.db import models
from django import forms
from django.contrib.auth import authenticate, login, logout

#For all choices, we want the dropdown value to be what's submitted in the form
#That's why we have duplicate entries

STUDY_PERIOD_LINK = (
    ('Profile', 'Profile'), ('Location', 'Location')
)

class LoginModel(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    login_date = models.DateTimeField(auto_now=True)


class DataEntryModel(models.Model):
    client_name = models.CharField(max_length=100)
    study_date = models.DateField(default='2001-01-01', help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_name = models.CharField(max_length=40, help_text='Enter a short description of the study')
    analyst_name = models.CharField(max_length=50)
    csv_file = models.FileField(upload_to='satool/')


class StudyPeriodModel(models.Model):
    study_period_start_1 = models.DateField(default='2001-01-01', help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_start_2 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_start_3 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_start_4 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_end_1 = models.DateField(default='2001-01-01', help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_end_2 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_end_3 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    study_period_end_4 = models.DateField(null=True, blank=True, help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    minimum_days_1 = models.IntegerField()
    minimum_days_2 = models.IntegerField(null=True, blank=True)
    minimum_days_3 = models.IntegerField(null=True, blank=True)
    minimum_days_4 = models.IntegerField(null=True, blank=True)
    study_period_link_1 = models.CharField(max_length=10, choices=STUDY_PERIOD_LINK)
    study_period_link_2 = models.CharField(max_length=10, blank=True, choices=STUDY_PERIOD_LINK)
    study_period_link_3 = models.CharField(max_length=10, blank=True, choices=STUDY_PERIOD_LINK)
    study_period_link_4 = models.CharField(max_length=10, blank=True, choices=STUDY_PERIOD_LINK)



