"""quiz_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from Quiz_arena import views
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.login, name = 'login'),
    #url(r'^home/$', views.home, name = 'home'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^signup/$',views.signup, name= 'signup'),
    url(r'^signin/$',views.signin, name='signin'),
    url(r'^if_unique/$',views.if_already_registered, name='if_unique'),
    url(r'^users/$',views.users_infos,name='user_infos'),
    url(r'^create_quiz/$',views.create_quiz,name='create_quiz'),
    url(r'^create_question/$',views.create_question,name='create_question'),
    url(r'^play/$',views.play,name='play'),
    url(r'^quiz_data/',views.push_quizData,name='push_quizData'),
    url(r'^register_response/',views.register_response,name='register_response'),
    #url(r'^check/$',views.check_session,name='check_session'),
    url(r'^quiz_links/$',views.quiz_links,name='quiz_links'),
    url(r'^leader_board/',views.leader_board,name='leader_board'),
]
