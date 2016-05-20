from __future__ import unicode_literals
from django.db import models

class ProjectMapper(models.Model):
    openhub = models.CharField(max_length=120)
    github = models.CharField(max_length=120)

