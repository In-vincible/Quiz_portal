from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms
from social.apps.django_app.default.models import UserSocialAuth
from datetime import timedelta
question_types = (('sc','sc'),('mc','mc'))


def filepath(self, filename):
    return '%s' % filename









class user_info(models.Model):
	user = models.OneToOneField(User, null = True)
	social_user = models.OneToOneField(UserSocialAuth, null = True)
	email = models.CharField(max_length = 50, unique = True)
	phone_no = models.CharField(max_length = 12, null = True)
	#skills = models.ForeignKey('skill', null = True, blank = True)
	profile_pic = models.ImageField(upload_to = filepath, default = 'index.png')
	about_me = models.TextField(default = 'I am a quizer !')
	
	def __unicode__(self):
		return u'%s %s' % (self.email, self.phone_no)
'''
class skill(models.Model):
	skill_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	proficiency = models.IntegerField(default = 50)
# Create your models here.
'''




class quiz(models.Model):
	quiz_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length=50)
	beginning_quote = models.TextField(null = True)
	end_quote = models.TextField(null = True)
	duration = models.IntegerField(default = 30)
	created_on = models.DateTimeField(auto_now = True)
	creator = models.ForeignKey(User,null = True)
	def __unicode__(self):
		return u'%s' % self.name

class questions(models.Model):
	question_id = models.AutoField(primary_key = True)
	quiz = models.ForeignKey(quiz,null = True)
	question_type = models.CharField(max_length = 10, choices = question_types, default = 'sc')
	question_title = models.TextField()
	correct_message = models.TextField(null  = True)
	Incorrect_message = models.TextField(null = True)

class options(models.Model):
	option_id = models.AutoField(primary_key = True)
	option_quote = models.CharField(max_length = 250)
	option_status = models.SmallIntegerField(default=0)
	question = models.ForeignKey(questions,null = True)


class quiz_response(models.Model):
	response_id = models.AutoField(primary_key = True)
	quiz = models.ForeignKey(quiz,null=True)
	user = models.ForeignKey(User,null=True)

class question_response(models.Model):
	response_id = models.AutoField(primary_key = True)
	question = models.ForeignKey(questions,null = True)
	quiz = models.ForeignKey(quiz_response,null = True)

class option_response(models.Model):
	response_id = models.AutoField(primary_key = True)
	option = models.ForeignKey(options,null = True)
	question = models.ForeignKey(question_response,null = True)