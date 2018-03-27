from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Teacher(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	fullname = models.CharField(max_length=255)
	# teacher identity card number
	ticnumber = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now=True)
		
	class Meta:
		ordering = ['date_created']

class Problem(models.Model):
	limited_questions = models.CharField(max_length=2048,blank=True)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	flag = models.CharField(max_length=255)
	keyword = models.CharField(max_length=255)
	point = models.IntegerField(default=0)
	attachment = models.FileField(upload_to='static/media/problem/attachment', default='static/media/problem/attachment/default.pcap')
	picture = models.FileField(upload_to='static/media/problem/picture', default='static/media/problem/picture/default.jpg')
	date_created = models.DateTimeField(auto_now=True)

	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

	def limited_questions_split_by_newline(self):
		return self.limited_questions.replace('\n\n','\n').split('\n')

class Support(models.Model):
	title = models.CharField(max_length=255)
	post = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now=True)

	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

class Evaluation(models.Model):
	difficult_level = models.CharField(max_length=255)
	difficult_forecast = models.CharField(max_length=255)
	picture = models.FileField(upload_to='static/media/problem/evaluation/picture', default='static/media/problem/evaluation/picture/default.jpg')
	question = models.CharField(max_length=255)
	A = models.CharField(max_length=255)
	B = models.CharField(max_length=255)
	C = models.CharField(max_length=255)
	D = models.CharField(max_length=255)
	E = models.CharField(max_length=255)
	answer = models.CharField(max_length=255)
	point = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now=True)

	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

	class Meta:
		ordering = ['date_created']

