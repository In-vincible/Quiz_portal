from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import user_info
# from django.template.context import RequestContext


def login(request):
	if 'logged_in' in request.session:
		if request.session['logged_in']:
			return render(request,'home.html')
		else:
			return render(request, 'index.html')
	else:
		return render(request, 'index.html')
def signup(request):
	if request.method == 'POST':
		post = request.POST
		if post['query'] == 'signup':
			user = User.objects.create_user(username=str(hash(post['form-email'])), email = post['form-email'],password = str(hash(post['password'])))
			user.first_name = post['form-first-name']
			user.last_name = post['form-last-name']
			user.save()
			User_info = user_info(user = user, email = post['form-email'], phone_no = post['form-number'])
			User_info.save()
	return render(request, 'registered.html',{'first_name':post['form-first-name'], 'email':post['form-email']})

def signin(request):
	if request.method == 'POST':
		post = request.POST
		if post['query'] == 'signin':
			
			user = authenticate(username = str(hash(post['username'])), password = str(hash(post['password'])))
			if user is not None:
				#print 'gotchaa'
				request.session['logged_in'] = True;
				request.session['username'] = str(post['username'])
				return render(request,'home.html',{'email': post['username']})
			else:
				return redirect('login')
		else:
			return redirect('login')
@login_required(login_url='/')
def home(request):
    return render_to_response('base.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
