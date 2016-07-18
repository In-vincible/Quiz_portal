from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import user_info
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.template.context import RequestContext
server = 'http://127.0.0.1:8000/'

def login(request):
	if 'logged_in' in request.session:
		if request.session['logged_in']:
			return render(request,'home.html')
		else:
			return render(request, 'index.html',{'server':server})
	else:
		return render(request, 'index.html',{'server':server})
def signup(request):
	if request.method == 'POST':
		post = request.POST
		if post['query'] == 'signup':
			user = User.objects.create_user(username=str(hash(post['email'])), email = post['email'],password = str(hash(post['password'])))
			user.first_name = post['first_name']
			user.last_name = post['last_name']
			user.save()
			User_info = user_info(user = user, email = post['email'], phone_no = post['number'])
			User_info.save()
			return render(request, 'registered.html',{'first_name':post['first_name'], 'email':post['email']})
		else:
			return redirect('login')
	else:
		return redirect('login')

def signin(request):
	if request.method == 'POST':
		post = request.POST
		if post['query'] == 'signin':
			
			user = authenticate(username = str(hash(post['username'])), password = str(hash(post['password'])))
			if user is not None:
				#print 'gotchaa'
				request.session['logged_in'] = True;
				request.session['username'] = post['username']
				return render(request,'home.html')
			else:
				return render(request,"index.html",{"errors":"Email or password not matching !","server":server})
		else:
			return redirect('login')
	else:
		return redirect('login')
'''
@login_required(login_url='/')
def home(request):
   return render_to_response('base.html')
'''

def logout(request):
	request.session['logged_in'] = False
	request.session['username'] = ''
	auth_logout(request)
	return redirect('/')
@csrf_exempt
def if_already_registered(request):
	if request.method == 'POST':
		post = request.POST
		val = post['value']
		if post['query'] == 'email':
			if User.objects.filter(email=val).exists():
				return HttpResponse(0)
			else:
				return HttpResponse(1)
		elif post['query'] == 'number':
			if user_info.objects.filter(phone_no=val).exists():
				return HttpResponse(0)
			else:
				return HttpResponse(1)

	
