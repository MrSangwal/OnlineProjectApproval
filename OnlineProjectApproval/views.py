from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.sessions.models import Session
import re
import os
import datetime

from .models import BRANCH
from .models import STUDENT
from .models import TEACHER
from .models import TITLE
from .models import PROJECT
from .models import PREVPROJECTS

# Create your views here.
def home(request):
	return render(request, 'home.html')

# Student Login & Registration Page
def student(request):
	a = BRANCH.objects.order_by('name')
	
	if request.session.has_key('roll'):
		del request.session['roll']
	return render(request, 'student.html', {'a':a})

# Teacher login & registration Page
def teacher(request):
	a = BRANCH.objects.order_by('name')
	
	if request.session.has_key('tid'):
		del request.session['tid']
	return render(request, 'teacher.html', {'a':a})

# ---------------- Student Registration Function Start--------------------
def Sregistration(request):
	uid = request.POST.get('userid')
	name = request.POST.get('name')
	branch = request.POST.get('branch')
	roll = request.POST.get('rollno')
	email = request.POST.get('email')
	pswd = request.POST.get('password')
	password = request.POST.get('confirm')
	question = request.POST.get('question')
	answer = request.POST.get('answer')
	getbranch = BRANCH.objects.all()

	if len(uid)==0 or len(name)==0 or len(branch)==0 or len(roll)==0 or len(email)==0 or len(pswd)==0 or len(password)==0 or len(question)==0 or len(answer)==0:
		messages.error(request, "!! Please Fill All fields !!")
		return redirect(student)

	if uid.isspace() or name.isspace() or branch.isspace() or roll.isspace() or email.isspace() or pswd.isspace() or password.isspace() or question.isspace() or answer.isspace():
		messages.error(request, "!! Please Enter Correct Value !!")
		return redirect(student)

	x = re.findall("\s", uid)
	if x:
		messages.error(request, "!! Please Enter UserID without Space. !!")
		return redirect(student)
	if len(roll)>12 or len(roll)<10:
		messages.error(request, "!! Enter a Valid Roll No. !!")
		return redirect(student)
	if pswd != password:
		messages.error(request, "!! Passwords Do Not Match !!")
		return redirect(student)

	if STUDENT.objects.filter(UserId = uid).exists():
		messages.error(request, "!! UserId Already Exists Use Another One !!")
		return redirect(student)

	if STUDENT.objects.filter(Rollno = roll).exists():
		messages.error(request, "!! User with this Roll NO Already Exists !!")
		return redirect(student)

	sql = STUDENT(UserId=uid, Name=name, Branch=BRANCH.objects.get(name=branch), Rollno=roll, Email=email, Password=password, Question=question, Answer=answer)
	sql.save()
	messages.success(request,"Registered Successfully")
	return redirect(student)

# ---------------- Student Registration Function ENDS --------------------\

# ---------------- Teacher Registration Function Start--------------------

def Tregistration(request):
	uid = request.POST.get('userid')
	name = request.POST.get('name')
	branch = request.POST.get('branch')
	email = request.POST.get('email')
	pswd = request.POST.get('password')
	password = request.POST.get('confirm')
	question = request.POST.get('question')
	answer = request.POST.get('answer')
	
	if len(uid)==0 or len(name)==0 or len(branch)==0 or len(email)==0 or len(pswd)==0 or len(password)==0 or len(question)==0 or len(answer)==0:
		messages.error(request, "Please Fill All fields")
		return redirect(teacher)

	if uid.isspace() or name.isspace() or branch.isspace() or email.isspace() or pswd.isspace() or password.isspace() or question.isspace() or answer.isspace():
		messages.error(request, "Please Enter Correct Value...")
		return redirect(teacher)

	x = re.findall("\s", uid)
	if x:
		messages.error(request, "Please Enter UserID without Space.")
		return redirect(teacher)
	if pswd != password:
		messages.error(request, "Passwords Do Not Match")
		return redirect(teacher)

	if TEACHER.objects.filter(UserId = uid).exists():
		messages.error(request, "!! User Already Exists !!")
		return redirect(teacher)

	if TEACHER.objects.filter(Branch = branch).exists():
		messages.error(request, "!! HOD of '"+branch.upper()+"' Branch Already Exist !!")
		return redirect(teacher)

	sql = TEACHER(UserId=uid, Name=name, Branch=BRANCH.objects.get(name=branch), Email=email, Password=password, Question=question, Answer=answer)
	sql.save()
		
	messages.success(request,"Registered Successfully.")
	return redirect(teacher)

# ---------------- Teacher Registration Function ENDS --------------------

# ---------------- Student Login Function Start--------------------

def Slogin(request):
	getuser=STUDENT.objects.all()
	uid = request.POST.get('userid')
	roll = request.POST.get('rollno')
	password = request.POST.get('password')

	if len(uid)==0 or len(roll)==0 or len(password)==0:
		messages.error(request, "Please Fill All fields")
		return redirect(student)

	x = re.findall("\s", uid)
	if x:
		messages.error(request, "Please Enter UserID without Space.")
		return redirect(student)

	if len(roll)>12 or len(roll)<10:
		messages.error(request, "Invalid Roll No.")
		return redirect(student)

	if STUDENT.objects.filter(Rollno = roll).exists():
		getuser= STUDENT.objects.all().filter(Rollno = roll)
		for i in getuser:
			if i.UserId != uid:
				messages.error(request, "!! UserId Do Not Match !!")
				return redirect(student)
			if i.Password != password:
				messages.error(request, "!! Wrong Password !!")
				return redirect(student)
			request.session['roll']=roll
			request.session['sid']=uid
			return redirect(dashboard)
	else:
		messages.error(request, "!! User Do Not Exists !!")
		return redirect(student)

# ---------------- Student Login Function ENDS --------------------

# ---------------- Teacher Login Function Start--------------------

def Tlogin(request):
	uid = request.POST.get('userid')
	password = request.POST.get('password')

	if len(uid)==0 or len(password)==0:
		messages.error(request, "Please Fill All fields")
		return redirect(teacher)

	x = re.findall("\s", uid)
	if x:
		messages.error(request, "Please Enter UserID without Space.")
		return redirect(teacher)

	if TEACHER.objects.filter(UserId = uid).exists():
		getuser= TEACHER.objects.all().filter(UserId = uid)
		for i in getuser:
			if i.Password != password:
				messages.error(request, "!! Wrong Password !!")
				return redirect(teacher)
			request.session['tid']=uid
			return redirect(Tdashboard)
	else:
		messages.error(request, "!! User Do Not Exists !!")
		return redirect(teacher)

# ---------------- Teacher Login Function ENDS --------------------

# ---------------- Student Dashboard Starts --------------------

def dashboard(request):
	if request.session.has_key('roll'):
		sessionid=request.session['roll']
		studentid=request.session['sid']
		user = STUDENT.objects.filter(Rollno = sessionid)
		branches = BRANCH.objects.all()
		for i in user:
			name = i.Name
			branch = str(i.Branch)
		for i in branches:
			if i.name == branch:
				chatfile=i.chatfile
		titles=TITLE.objects.filter(Rollno=sessionid).order_by('-id')
		titlesup=TITLE.objects.filter(Rollno=sessionid, Status='Approved').order_by('-id')
		project=PROJECT.objects.filter(Rollno=sessionid).order_by('-id')
		projectup=PROJECT.objects.filter(Rollno=sessionid, Status='Approved').order_by('-id')
		chat_file = "static/"+chatfile
		return render(request, 'Sdashboard.html', {'roll':sessionid, 'sid':studentid,'title':titles,'titleup':titlesup, 'project':project, 'projectup':projectup, 'chat':chat_file})
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Dashboard Ends --------------------

# ---------------- Student Profile Starts --------------------

def profile(request):
	if request.session.has_key('roll'):
		sessionid=request.session['roll']
		getinfo = STUDENT.objects.filter(Rollno = sessionid)
		return render(request, 'Sprofile.html', {'sid':sessionid, 'info':getinfo})
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Profile Ends --------------------

# ---------------- Student Update Profile Starts --------------------

def update_student(request):
	if request.session.has_key('roll'):
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		question = request.POST.get('question')
		answer = request.POST.get('answer')
		sessionid=request.session['roll']
		studentid=request.session['sid']

		if len(name)<3 or name.isspace():
			messages.error(request, "Enter a Valid Name")
			return redirect(profile)
		if phone == "":
			phone = None
		update = STUDENT.objects.get(Rollno = sessionid, UserId = studentid)

		try:
			photo=request.FILES['pic']
		except:
			pass
		else:
			if update.Pic != None:
				if update.Pic != 'images/profile.jpg' :
					update.Pic.delete(save=True)
			update.Pic = request.FILES['pic']
		update.Name = name
		update.Email = email
		update.Mobile = phone
		update.Question = question
		update.Answer = answer
		update.save()
		messages.success(request, " Profile Updated Successfully ")
		return redirect(profile)
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Update Profile Ends --------------------

# ---------------- Student Remove Profile Starts --------------------

def remove_profile(request):
	if request.session.has_key('roll'):
		sessionid=request.session['roll']
		get = STUDENT.objects.filter(Rollno = sessionid)
		for i in get:
			if i.Pic != None:
				if i.Pic != 'images/profile.jpg' :
					i.Pic.delete(save=True)
					i.Pic = 'images/profile.jpg'
					i.save()
					messages.success(request, "image deleted successfully")
				else:
					messages.error(request, "Image Not found.")
		return redirect(profile)
	elif request.session.has_key('tid'):
		sessionid=request.session['tid']
		get = TEACHER.objects.filter(UserId = sessionid)
		for i in get:
			if i.Pic != None:
				if i.Pic != 'images/profile.jpg' :
					i.Pic.delete(save=True)
					i.Pic = 'images/profile.jpg'
					i.save()
					messages.success(request, "image deleted successfully")
				else:
					messages.error(request, "Image Not found.")
		return redirect(Tprofile)

# ---------------- Student Remove Profile Ends --------------------

# ---------------- Student Upload Title Starts --------------------

def upload_title(request):
	if request.session.has_key('roll'):
		sessionid=request.session['roll']
		return render(request, 'upload_title.html', {'sid':sessionid})
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Upload Title Ends --------------------

# ---------------- Student Title Uploading Function Starts --------------------

def title_upload(request):
	if request.session.has_key('roll'):
		title = request.POST.get('title')
		objective = request.POST.get('objective')
		roll = request.session['roll']
		d = datetime.datetime.now()
		date = d.strftime("%Y-%m-%d")
		gettitle=TITLE.objects.filter(Rollno=roll)

		if len(title)<1 or len(objective)<1:
			messages.error(request, "All fields are required.")
			return redirect(upload_title)
		if len(title)<5:
			messages.error(request, "Title length must be greater than 4 characters")
			return redirect(upload_title)
		if len(objective)>999:
			messages.error(request, "Objective length must be less than 1000 characters")
			return redirect(upload_title)
		getinfo = STUDENT.objects.filter(Rollno = roll)
		for i in getinfo:
			name = i.Name
			branch = i.Branch
		alltitles=list()
		for i in gettitle:
			alltitles.append(i.Title)
		if title in alltitles:
			i.Title = title
			i.Objective = objective
			i.Status = 'Pending'
			Date = date
			i.save()
			messages.success(request, "Title Uploaded.")
			return redirect(upload_title)
		else:
			sql = TITLE(Rollno =STUDENT.objects.get(Rollno=roll), Name = name, Branch = BRANCH.objects.get(name=branch), Title = title, Objective = objective, Status = 'Pending', Date = date )
			sql.save()
			messages.success(request, "Title Uploaded.")
			return redirect(upload_title)
	else:
		messages.error(request, "!! Login Required !!")
		return redirect(student)

# ---------------- Student Title Uploading Function Ends --------------------

# ------------------- View Title Starts ---------------------------

def view_title(request, titleid):
	if request.session.has_key('roll'):
		gettitle=TITLE.objects.filter(id=titleid)
		if gettitle:
			return render(request, 'title.html', {'title':gettitle})
		else:
			messages.error(request, "record not found")
			return redirect(dashboard)
	if request.session.has_key('tid'):
		uid = request.session['tid'];
		gettitle=TITLE.objects.filter(id=titleid)
		if gettitle:
			return render(request, 'title.html', {'uid':uid, 'title':gettitle})
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ------------------- View Title Ends ---------------------------

# ------------------- Teacher Approve Title Page Starts ---------------------------

def approve_title(request, titleid):
	if request.session.has_key('tid'):
		gettitle=TITLE.objects.filter(id=titleid)
		if gettitle:
			return render(request, 'approve_title.html', {'title':gettitle})
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Approve Title Page Ends ---------------------------

# ------------------- Teacher Approve Project Page Starts ---------------------------

def approve_project(request, projectid):
	if request.session.has_key('tid'):
		gettitle=PROJECT.objects.filter(id=projectid)
		if gettitle:
			return render(request, 'approve_project.html', {'title':gettitle})
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Approve Project Page Ends ---------------------------

# ------------------- Teacher Title Approve Function Starts ---------------------------

def title_approve(request, titleid):
	if request.session.has_key('tid'):
		titlecmt = request.POST.get('ttlcmt')
		objectivecmt = request.POST.get('objcmt')
		stats = 'Approved'
		if len(titlecmt)==0 or titlecmt.isspace() or len(objectivecmt)==0 or objectivecmt.isspace():
			messages.error(request, "Please Add Your Suggestions !")
			return redirect(Tdashboard)
		gettitle=TITLE.objects.filter(id=titleid)
		if gettitle:
			for i in gettitle:
				i.Tcomment = titlecmt
				i.Ocomment = objectivecmt
				i.Status = stats
				i.save()
			messages.success(request, "Title Approved Successfully.")
			return redirect(Tdashboard)
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Title Approve Function Ends ---------------------------

# ------------------- Teacher Project Approve Function Starts ---------------------------

def project_approve(request, projectid):
	if request.session.has_key('tid'):
		sugg = request.POST.get('prosugg')
		stats = 'Approved'
		getproject=PROJECT.objects.filter(id=projectid)
		if getproject:
			for i in getproject:
				i.Comment = sugg
				i.Status = stats
				i.save()
			messages.success(request, "Project Approved Successfully.")
			return redirect(Tdashboard)
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Project Approve Function Ends ---------------------------

# ------------------- Teacher Title Reject Function Starts ---------------------------

def title_reject(request, titleid):
	if request.session.has_key('tid'):
		titlecmt = request.POST.get('ttlcmt')
		objectivecmt = request.POST.get('objcmt')
		stats = 'Rejected'
		if len(titlecmt)==0 or titlecmt.isspace() or len(objectivecmt)==0 or objectivecmt.isspace():
			messages.error(request, "Please Add Your Suggestions !")
			return redirect(Tdashboard)
		gettitle=TITLE.objects.filter(id=titleid)
		if gettitle:
			for i in gettitle:
				i.Tcomment = titlecmt
				i.Ocomment = objectivecmt
				i.Tdelete = 'ON'
				i.Status = stats
				i.save()
			messages.success(request, "Title Rejected.")
			return redirect(Tdashboard)
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Title Reject Function Ends ---------------------------

# ------------------- Teacher Project Reject Function Starts ---------------------------

def project_reject(request, projectid):
	if request.session.has_key('tid'):
		sugg = request.POST.get('prosugg')
		stats = 'Rejected'
		getproject=PROJECT.objects.filter(id=projectid)
		if getproject:
			for i in getproject:
				i.Comment = sugg
				i.Status = stats
				i.save()
			messages.success(request, "Project Rejected.")
			return redirect(Tdashboard)
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ------------------- Teacher Project Reject Function Ends ---------------------------

# ---------------- Student Upload Project Page Starts --------------------

def upload_project(request):
	if request.session.has_key('roll'):
		sessionid=request.session['roll']
		return render(request, 'upload_project.html', {'sid':sessionid})
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Upload Project Page Ends --------------------

# ---------------- Student Project Uploading Function Starts --------------------

def project_upload(request):
	if request.session.has_key('roll'):
		title = request.POST.get('title')
		objective = request.POST.get('objective')
		roll = request.session['roll']
		file = request.POST.get('pfile')
		d = datetime.datetime.now()
		date = d.strftime("%Y-%m-%d")
		getproject=PROJECT.objects.filter(Rollno=roll)

		if len(title)<1 or len(objective)<1:
			messages.error(request, "All fields are required.")
			return redirect(upload_project)
		try:
			request.FILES['pfile']
		except:
			messages.error(request, 'Choose File')
			return redirect(upload_project)
		if len(title)<5:
			messages.error(request, "Title length must be greater than 4 characters")
			return redirect(upload_project)
		if len(objective)>999:
			messages.error(request, "Objective length must be less than 1000 characters")
			return redirect(upload_project)
		getinfo = STUDENT.objects.filter(Rollno = roll)
		for i in getinfo:
			name = i.Name
			branch = i.Branch
		allprojects=list()
		for i in getproject:
			allprojects.append(i.Title)
		if title in allprojects:
			i.Title = title
			i.Objective = objective
			i.Status = 'Pending'
			i.File = request.FILES['pfile']
			Date = date
			i.save()
			messages.success(request, "Title Uploaded.")
			return redirect(upload_project)
		else:
			sql = PROJECT(Rollno =STUDENT.objects.get(Rollno=roll), Name = name, Branch = BRANCH.objects.get(name=branch), Title = title, Objective = objective, File = request.FILES['pfile'], Status = 'Pending', Date = date )
			sql.save()
			messages.success(request, "Project Uploaded.")
			return redirect(upload_project)
	else:
		messages.error(request, "!! Login Required !!")
		return redirect(student)

# ---------------- Student Project Uploading Function Ends --------------------

# ------------------- View Title Starts ---------------------------

def view_project(request, projectid):
	if request.session.has_key('roll'):
		getproject=PROJECT.objects.filter(id=projectid)
		if getproject:
			return render(request, 'project.html', {'project':getproject})
		else:
			messages.error(request, "record not found")
			return redirect(dashboard)
	if request.session.has_key('tid'):
		uid = request.session['tid'];
		getproject=PROJECT.objects.filter(id=projectid)
		if getproject:
			return render(request, 'project.html', {'project':getproject, 'uid':uid})
		else:
			messages.error(request, "record not found")
			return redirect(Tdashboard)
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ------------------- View Title Ends ---------------------------

# ---------------- Student Previous Projects Page Starts --------------------

def prev_projects(request):
	if request.session.has_key('roll'):
		sid = request.session['roll']
		user = STUDENT.objects.filter(Rollno = sid)
		for i in user:
			branch = i.Branch
		projects = PREVPROJECTS.objects.filter(Branch = branch)
		return render(request, 'prev_projects.html', {'uid':sid, 'prevprojects':projects})
	else:
		messages.error(request, "! Login Required !")
		return redirect(student)

# ---------------- Student Previous Projects Page Ends --------------------

# ---------------- Teacher Dashboard Starts --------------------

def Tdashboard(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		user = TEACHER.objects.filter(UserId = sessionid)
		branches = BRANCH.objects.all()
		for i in user:
			branch = i.Branch
			name = i.Name
		for i in branches:
			if i.name == str(branch):
				chatfile=i.chatfile
		titlesp=TITLE.objects.filter(Status='Pending', Branch = branch).order_by('-id')
		projectsp=PROJECT.objects.filter(Status='Pending', Branch = branch).order_by('-id')
		chat_file = "static/"+chatfile
		return render(request, 'Tdashboard.html', {'tid':sessionid, 'titlep':titlesp, 'projectp':projectsp, 'chat_file':chat_file})
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Dashboard Ends --------------------

# ---------------- Teacher Profile Starts --------------------

def Tprofile(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		getinfo = TEACHER.objects.filter(UserId = sessionid)
		return render(request, 'Tprofile.html', {'tid':sessionid, 'info':getinfo})
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Profile Ends --------------------

# ---------------- Teacher Update Profile Starts --------------------

def update_teacher(request):
	if request.session.has_key('tid'):
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		question = request.POST.get('question')
		answer = request.POST.get('answer')
		sessionid=request.session['tid']

		if len(name)<3 or name.isspace():
			messages.error(request, "Enter a Valid Name")
			return redirect(profile)
		if phone == "":
			phone = None
		update = TEACHER.objects.get(UserId = sessionid)

		try:
			photo=request.FILES['pic']
		except:
			pass
		else:
			if update.Pic != None:
				if update.Pic != 'images/profile.jpg' :
					update.Pic.delete(save=True)
			update.Pic = request.FILES['pic']
		
		update.Name = name
		update.Email = email
		update.Mobile = phone
		update.Question = question
		update.Answer = answer
		update.save()
		messages.success(request, " Profile Updated Successfully ")
		return redirect(Tprofile)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Update Profile Ends --------------------

# ---------------- Teacher Approved Titles Starts --------------------

def approved_titles(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		user = TEACHER.objects.filter(UserId = sessionid)
		for i in user:
			branch = i.Branch
		gettitles=TITLE.objects.filter(Status = 'Approved', Branch = branch).order_by('Rollno')
		return render(request, 'approved_titles.html', {'tid':sessionid, 'title':gettitles})
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Approved Titles Ends --------------------

# ---------------- Teacher Submitted Projects Starts --------------------

def submitted_projects(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		user = TEACHER.objects.filter(UserId = sessionid)
		for i in user:
			branch = i.Branch
		getprojects=PROJECT.objects.filter(Status = 'Approved', Branch = branch).order_by('Rollno')
		return render(request, 'submitted_projects.html', {'tid':sessionid, 'project':getprojects})
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Submitted Projects Ends --------------------

# ---------------- Teacher Previous Projects Starts --------------------

def previous_projects(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		getbranch = TEACHER.objects.filter(UserId = sessionid)
		for i in getbranch:
			branch=i.Branch
		projects = PREVPROJECTS.objects.filter(Branch = branch)
		return render(request, 'previous_projects.html', {'tid':sessionid, 'prevprojects':projects})
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# ---------------- Teacher Previous Projects Ends --------------------

# ---------------- Upload Previous Projects Starts ------------------------

def upload_previous(request):
	if request.session.has_key('tid'):
		sessionid=request.session['tid']
		ptitle = request.POST.get('title')
		file = request.FILES['pfile']
		if len(ptitle)==0 or ptitle.isspace():
			messages.error(request, "All fields must be Filled !")
			return redirect(previous_projects)
		d = datetime.datetime.now()
		date = d.strftime("%Y-%m-%d")
		getinfo = TEACHER.objects.filter(UserId = sessionid)
		for i in getinfo:
			name = i.Name
			branch = i.Branch
		sql = PREVPROJECTS(Branch = BRANCH.objects.get(name=branch), Title = ptitle, File = file, Date = date )
		sql.save()
		messages.success(request, "Project Uploaded Successfully !")
		return redirect(previous_projects)
	else:
		messages.error(request, "! Login Required !")
		return redirect(teacher)

# Create Chat File and Update Chat
def chatme(request):
	if request.session.has_key('tid'):
		msg = request.POST.get('message')
		date = datetime.datetime.now()
		ctime = date.strftime("%d/%m/%y\t%H:%M")
		sessionid=request.session['tid']
		user = TEACHER.objects.filter(UserId = sessionid)
		branches = BRANCH.objects.all()
		for i in user:
			name = i.Name
			branch = str(i.Branch)
		for i in branches:
			if i.name == branch:
				chatfile=i.chatfile
				file = open("static/"+chatfile, "a")
				file.write('\n<div style="display:flex;flex-direction: column;margin: 0px;padding: 0px;width: 100%;">\n<div style="display:flex;flex-direction:row;width: 100%;padding: 5px 0px;">\n<h4 style="padding:0px 5px;margin:0px;font-weight:300;"><b>'+name+'</b></h4>\n<h5 style="padding:0px 5px;margin: 0px;margin-left: auto;font-weight:300">'+ctime+'</h5>\n</div>\n<div style="padding:3px 5px;font-size:16px">'+msg+'</div>\n</div>')
				file.close()
		return redirect(Tdashboard)

	elif request.session.has_key('roll'):
		msg = request.POST.get('message')
		date = datetime.datetime.now()
		ctime = date.strftime("%d/%m/%y\t%H:%M")
		sessionid=request.session['roll']
		user = STUDENT.objects.filter(Rollno = sessionid)
		branches = BRANCH.objects.all()
		for i in user:
			name = i.Name
			branch = str(i.Branch)
		for i in branches:
			if i.name == branch:
				chatfile=i.chatfile
				file = open("static/"+chatfile, "a")
				file.write('\n<div style="display:flex;flex-direction: column;margin: 0px;padding: 0px;width: 100%;">\n<div style="display:flex;flex-direction:row;width: 100%;padding: 5px 0px;">\n<h4 style="padding:0px 5px;margin:0px;font-weight:300;"><b>'+name+'</b></h4>\n<h5 style="padding:0px 5px;margin: 0px;margin-left: auto;font-weight:300">'+ctime+'</h5>\n</div>\n<div style="padding:3px 5px;font-size:16px">'+msg+'</div>\n</div>')
				file.close()
				return redirect(dashboard)
		messages.error(request,"File Not Found")
		return redirect(dashboard)
	else:
		messages.error(request,"Login Required")
		return redirect(student)

# Forget password Page
def forgetpassword(request, user):
	if user == "teacher":
		u = 'Teacher'
		return render(request, 'forgetpassword.html',{'u':u})
	else:
		return render(request, 'forgetpassword.html')

# Change password Page -- (Forget password)
def changepassword(request):
	if request.POST.get('userid'):
		uid = request.POST.get('userid')
		usr = 'teacher'
		x = re.findall("\s", uid)
		if x:
			messages.error(request, "Please Enter UserID without Space.")
			return redirect('forgetpassword', user=usr)
		elif uid.isspace() or uid=="":
			messages.error(request, "Please Enter UserID")
			return redirect('forgetpassword', user=usr)
		if TEACHER.objects.filter(UserId = uid).exists():
			myid = TEACHER.objects.filter(UserId=uid)
		else:
			messages.error(request, "No User with this UserID")
			return redirect('forgetpassword', user = usr)

	elif request.POST.get('rollno'):
		uid = request.POST.get('rollno')
		usr = 'student'
		if uid.isspace() or uid=="":
			messages.error(request, "Please Enter Rollno")
			return redirect('forgetpassword', user=usr)
		if STUDENT.objects.filter(Rollno = uid).exists():
			myid = STUDENT.objects.filter(Rollno=uid)
		else:
			messages.error(request, "No User with this Roll No")
			return redirect('forgetpassword',user=usr)
	else:
		messages.error(request, "User Details Not Found.")
		return redirect(home)

	if myid != None or myid != "":
		question = request.POST.get('question')
		answer = request.POST.get('answer')
		if question.isspace() or question=="":
			messages.error(request, "Please Enter Question")
			return redirect('forgetpassword', user=usr)
		if answer.isspace() or answer=="":
			messages.error(request, "Please Enter Answer")
			return redirect('forgetpassword', user=usr)
		for i in myid:
			ques = i.Question
			ans = i.Answer
		if question != ques or answer != ans:
			messages.error(request,"Incorrect Question and Answer")
			return redirect('forgetpassword', user=usr)
		cpd = request.session['cpid']=uid
		return render(request, 'changepassword.html',{'id':cpd})

# Password Change Function --(Forget Password)
def passwordchange(request):
	if request.session.has_key('cpid'):
		uid = request.session['cpid']
		if uid.isnumeric():
			user= STUDENT.objects.get(Rollno=uid)
			u='student'
		else:
			user = TEACHER.objects.get(UserId=uid)
			u='teacher'
		pswd=request.POST.get('password')
		password=request.POST.get('cpassword')
		if pswd.isspace() or password.isspace() or pswd=='' or password=='':
			messages.error(request,"Please Fill All Fields")
			return redirect('forgetpassword',user=u)
		elif pswd != password:
			messages.error(request,"Passwords Do Not Match !")
			return redirect('forgetpassword',user=u)
		else:
			user.Password = password
			user.save()
			messages.success(request,'Password Changed Successfully !')
			del request.session['cpid']
			if u=="teacher":
				return redirect(teacher)
			else:
				return redirect(student)
	else:
		messages.error(request,"Page Not Found")
		return redirect(home)


# Change Password Page From Profile
def updatepassword(request):
	if request.session.has_key('roll'):
		return render(request, 'updatepassword.html')
	elif request.session.has_key('tid'):
		return render(request, 'updatepassword.html')
	else:
		messages.error(request,"Login Required !")
		return redirect(student)

# Update Password Function & redirect to login page
def passwordupdate(request):
	if request.session.has_key('roll'):
		uid=request.session['roll']
		user = STUDENT.objects.get(Rollno=uid)
	elif request.session.has_key('tid'):
		uid=request.session['tid']
		user = TEACHER.objects.get(UserId=uid)
	else:
		messages.error(request,"Login Required !")
		return redirect(student)
	oldpassword = user.Password
	oldpswd=request.POST.get('oldpassword')
	pswd=request.POST.get('password')
	password=request.POST.get('cpassword')

	if oldpswd.isspace() or pswd.isspace() or password.isspace() or oldpswd=='' or pswd=='' or password=='':
		messages.error(request,"All Fields are Required !")
		return redirect(updatepassword)
	elif oldpswd != oldpassword:
		messages.error(request,"Old Password Does Not Match !")
		return redirect(updatepassword)
	elif pswd != password:
		messages.error(request,"New Passwords Do Not Match !")
		return redirect(updatepassword)
	else:
		user.Password = password
		user.save()
		messages.success(request,"Password Updated Successfully")
		if uid.isnumeric():
			return redirect(student)
		else:
			return redirect(teacher)
