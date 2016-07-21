from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import user_info,quiz,options,questions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from django.template.context import RequestContext
server = 'https://quiz-portal.herokuapp.com/' #'http://127.0.0.1:8000/'

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

def users_infos(request):
	users = user_info.objects.all()
	quizes = quiz.objects.all()
	phone_nos = ''
	Questions = questions.objects.all()
	Options = options.objects.all()
	opa = ''
	for o in Options:
		opa += o.option_quote
		print o.option_quote,o.option_status
	for Q in Questions:
		print Q.question_title
		print Q.question_type
	for q in quizes:
		print q.name
	for user in users:
		print user.phone_no
		phone_nos += "<br>  " + user.phone_no
	return HttpResponse(phone_nos+opa)

def create_quiz(request):
	if 'logged_in' in request.session:
		if request.session['logged_in'] and request.method == 'POST':
			post = request.POST
			user = User.objects.get(email = request.session['username'])
			Quiz = quiz(name=post['quiz_name'],beginning_quote=post['beginning_quote'],end_quote=post['end_quote'],creator=user,duration=post['duration']) 
			Quiz.save()
			return render(request,'quiz_created.html',{'quiz':Quiz,'server':server})

@csrf_exempt
def create_question(request):
	if 'logged_in' in request.session:
		if request.session['logged_in'] and request.method == 'POST':
			post = request.POST
			#post = json.loads(post)
			Quiz = quiz.objects.get(quiz_id=post['quiz_id'])
			Question = questions(quiz=Quiz,question_type=post['question_type'],question_title=post['question_title'],correct_message=post['correct_message'],Incorrect_message=post['incorrect_message'])
			Question.save()
			Options = json.loads(post['options'])
			for option in Options:#post['options']:
				print option
				Option = options(option_quote=option['value'],option_status=option['status'],question=Question)
				Option.save()
			return HttpResponse("Question Added Successfully")
		else:
			return HttpResponse("Invalid User")
	else:
		return redirect("login")
@csrf_exempt
def push_quizData(request):
	if 'logged_in' in request.session:
		if request.session['logged_in'] and request.method == 'GET':
			id = request.GET['quiz_id']
			Quiz = quiz.objects.get(quiz_id=id)
			data = {}
			info = {}
			info['name'] = Quiz.name
			info['main'] = "<p>" +Quiz.beginning_quote+"</p>"
			info['results'] = "<h5>Learn more</h5><p>"+Quiz.end_quote+"</p>"
			info['level1'] = "Genius"
			info['level2'] = "Tending to Genius"
			info['level3'] = "Amateur"
			info['level4'] = "Newbie :p"
			info['level5'] = "Stay in school, Kid..."
			data['info'] = info
			json_questions = []
			Questions = questions.objects.filter(quiz=Quiz)

			for Question in Questions:
				json_question = {}
				json_question['q'] = Question.question_title
				Options = options.objects.filter(question=Question)
				json_options = []
				for Option in Options:
					json_option = {}
					json_option['option'] = Option.option_quote
					if Option.option_status:
						json_option['correct'] = True
					else:
						json_option['correct'] = False
					json_options.append(json_option)
				json_question['a'] = json_options
				if Question.question_type == 'sc':
					json_question['select_any'] = True

				json_question['correct'] = "<p><span>Correct !</span>"+Question.correct_message+"</p>"
				json_question['incorrect'] = "<p><span>Incorrect !</span>"+Question.Incorrect_message+"</p>"
				json_questions.append(json_question)
			data['questions'] = json_questions
			return JsonResponse(data)


def play(request):
	if 'logged_in' in request.session:
		if request.session['logged_in'] and request.GET['quiz_id']:
			return render(request,'quiz.html',{'id':request.GET['quiz_id'],"server":server})

