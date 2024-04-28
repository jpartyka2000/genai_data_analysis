from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone


class EasyQueryStudies(models.Model):
    study_id = models.IntegerField(primary_key=True)
    study_name = models.CharField(max_length=80)
    created_by = models.IntegerField()
    created_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'easyquery_studies'


class EasyQueryHistory(models.Model):
    """Model representing a user session history."""
    df_html_str_req = models.TextField()
    user_question = models.TextField(blank=True)
    output_str = models.TextField(blank=True)
    df_html_str_res = models.TextField(blank=True)
    study_name = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = 'easyquery_history'
        ordering = ['id']
