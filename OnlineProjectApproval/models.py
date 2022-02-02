from django.db import models

# Create your models here.

class BRANCH(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	chatfile = models.CharField(max_length=100, default='file')

	def __str__(self):
		return self.name

class STUDENT(models.Model):
	UserId = models.CharField(max_length=50)
	Name = models.CharField(max_length=50)
	Branch = models.ForeignKey(BRANCH, on_delete=models.CASCADE)
	Rollno = models.CharField(max_length=12, primary_key=True)
	Email = models.EmailField(max_length=150)
	Mobile = models.BigIntegerField(null=True)
	Password = models.CharField(max_length=50)
	Question = models.CharField(max_length=100)
	Answer = models.CharField(max_length=50)
	Pic = models.FileField(upload_to='images', default='images/profile.jpg')

	def __str__(self):
		return self.Rollno

class TEACHER(models.Model):
	UserId = models.CharField(max_length=50, primary_key=True)
	Name = models.CharField(max_length=50)
	Branch = models.ForeignKey(BRANCH, on_delete=models.CASCADE)
	Email = models.EmailField(max_length=150)
	Mobile = models.BigIntegerField(null=True)
	Password = models.CharField(max_length=50)
	Question = models.CharField(max_length=100)
	Answer = models.CharField(max_length=50)
	Pic = models.FileField(upload_to='images', default='images/profile.jpg')
	
	def __str__(self):
		return self.Name


class TITLE(models.Model):
	id = models.AutoField(primary_key=True)
	Rollno = models.ForeignKey(STUDENT, on_delete=models.CASCADE)
	Name = models.CharField(max_length=50)
	Branch = models.ForeignKey(BRANCH, on_delete=models.CASCADE)
	Title = models.CharField(max_length=100)
	Tcomment = models.CharField(max_length=250, null=True)
	Objective = models.CharField(max_length=1000)
	Ocomment = models.CharField(max_length=250, null=True)
	Sdelete = models.CharField(max_length=3, default='OFF')
	Tdelete = models.CharField(max_length=3, default='OFF')
	Status = models.CharField(max_length=50)
	Date = models.DateField()


class PROJECT(models.Model):
	id = models.AutoField(primary_key=True)
	Rollno = models.ForeignKey(STUDENT, on_delete=models.CASCADE)
	Name = models.CharField(max_length=50)
	Branch = models.ForeignKey(BRANCH, on_delete=models.CASCADE)
	Title = models.CharField(max_length=100)
	Objective = models.CharField(max_length=1000)
	File = models.FileField(upload_to='projects')
	Comment = models.CharField(max_length=250, null=True)
	Sdelete = models.CharField(max_length=3, default='OFF')
	Tdelete = models.CharField(max_length=3, default='OFF')
	Status = models.CharField(max_length=50)
	Date = models.DateField()

class PREVPROJECTS(models.Model):
	id = models.AutoField(primary_key=True)
	Branch = models.ForeignKey(BRANCH, on_delete=models.CASCADE)
	Title = models.CharField(max_length=100)
	File = models.FileField(upload_to='prev_projects')
	Date = models.DateField()