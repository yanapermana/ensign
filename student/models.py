from __future__ import unicode_literals

from django.db import models
from teacher.models import Problem, Evaluation

class Student(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	salt = models.CharField(max_length=255, default='salt_value')
	fullname = models.CharField(max_length=255)
	# student identity card number
	sicnumber = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now=True)
		
	class Meta:
		ordering = ['date_created']

class Team(models.Model):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default='confirmed')
	invitation_code = models.CharField(max_length=255)
	point = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now=True)

	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

class Writeup(models.Model):
	known_list = models.CharField(max_length=255)
	unknown_list = models.CharField(max_length=255)
	todo_list = models.CharField(max_length=255)
	problem_statement = models.CharField(max_length=255)
	conclusion = models.CharField(max_length=255)
	answer = models.CharField(max_length=255)
	point = models.IntegerField(default=0)
	teacher_point = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now=True)

	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

class Solve(models.Model):
	status = models.BooleanField(default=False)
	tries = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now=True)

	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

class Evsolv(models.Model):
	status = models.BooleanField(default=False)
	attempt = models.BooleanField(default=False)
	tries = models.IntegerField(default=0)

	date_created = models.DateTimeField(auto_now=True)

	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']