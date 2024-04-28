from django import forms
from django.forms.widgets import Input
import re


class EasyQueryInputForm(forms.Form):
    study_name = forms.CharField(label='Study Name:', max_length=80, help_text='Enter a short description of the study')
    csv_file = forms.FileField(label='Load a new spreadsheet (must be CSV format):',widget=forms.ClearableFileInput())
