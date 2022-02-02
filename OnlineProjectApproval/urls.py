"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('student', views.student),
    path('forgetpassword<str:user>', views.forgetpassword, name='forgetpassword'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('newpassword', views.passwordchange),
    path('mypassword', views.updatepassword),
    path('mynewpassword', views.passwordupdate),
    path('teacher', views.teacher),
    path('Dashboard', views.dashboard),
    path('Sregistration', views.Sregistration),
    path('Tregistration', views.Tregistration),
    path('Slogin', views.Slogin),
    path('Tlogin', views.Tlogin),
    path('Sprofile', views.profile),
    path('update_student', views.update_student),
    path('update_teacher', views.update_teacher),
    path('remove_profile', views.remove_profile),
    path('upload_title', views.upload_title),
    path('title_upload', views.title_upload),
    path('Approve<int:titleid>', views.approve_title, name="approve"),
    path('title_approve<int:titleid>', views.title_approve, name="titleapprove"),
    path('title_reject<int:titleid>', views.title_reject, name="titlereject"),
    path('Title<int:titleid>', views.view_title, name="view"),
    path('Project<int:projectid>', views.approve_project, name="proapprove"),
    path('project_approve<int:projectid>', views.project_approve, name="projectapprove"),
    path('project_reject<int:projectid>', views.project_reject, name="projectreject"),
    path('Projectview<int:projectid>', views.view_project, name="viewproject"),
    path('upload_project', views.upload_project),
    path('project_upload', views.project_upload),
    path('prev_projects', views.prev_projects),
    path('Tdashboard', views.Tdashboard),
    path('Tprofile', views.Tprofile),
    path('approved_titles', views.approved_titles),
    path('submitted_projects', views.submitted_projects),
    path('previous_projects', views.previous_projects),
    path('upload_previous', views.upload_previous),
    path('chatme', views.chatme),
]
