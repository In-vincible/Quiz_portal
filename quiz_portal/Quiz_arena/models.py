from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms
class user_info(models.Model):
	user = models.OneToOneField(User, null = True)
	email = models.CharField(max_length = 50, unique = True)
	phone_no = models.CharField(max_length = 12, null = True)
	def __unicode__(self):
		return u'%s %s' % (self.email, self.phone_no)

# Create your models here.
