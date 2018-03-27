# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from student.models import Student, Team, Writeup, Solve, Evsolv
from teacher.models import Problem, Support, Evaluation
from student.defs import generate_invitation_code, password_hashing
from teacher.defs import bbcodetohtml

from django import template
from django.core.urlresolvers import reverse

import os
import binascii
import datetime
import string
import collections
import operator

# VALIDATION
def numval(strings):
	for s in strings:
		if s not in string.digits:
			return False
	return True

def fullnameval(strings):
	charset = string.ascii_letters + ' '
	for s in strings:
		if s not in charset:
			return False
	return True

def index(request):
	data = {'title_tag':'ENSIGN | Login'}
	data.update(csrf(request))
	return render_to_response('student/login.html', data)

def about(request):
	data = {'title_tag':'ENSIGN | About'}
	return render_to_response('student/about.html', data)

def login_error(request):
	data = {'title_tag':'ENSIGN | Login'}
	data.update(csrf(request))
	return render_to_response('student/login_error.html', data)
	
def login(request):
	try:		
		username = request.POST.get('username')
		password = request.POST.get('password')
		S = Student.objects.get(username=username)
		password, salt = password_hashing(password, binascii.unhexlify(S.salt))
		auth = Student.objects.filter(username__exact=username, password__exact=password)
		print auth[0].password, password
		if auth[0].username == username and auth[0].password == password :
			request.session['Student_id'] = auth[0].id
			return redirect('/student/welcome')
	except:
		pass
	return redirect('/student/login_error')

def welcome(request):
	try:
		if request.session['Student_id']:
			data = {'title_tag':'ENSIGN | Welcome'}
			data['message'] = "['Welcome to ENSIGN', 'Please read this guide.']"
			data['icon'] = 'info'
			data['heading'] = 'Info'
			return render_to_response('student/welcome.html', data)
	except:
		pass
	return redirect('/student/login')

def guide(request):
	try:
		if request.session['Student_id']:
			data = {'title_tag':'ENSIGN | Guide'}
			data['message'] = "['Welcome to ENSIGN', 'Please read this guide...']"
			data['icon'] = 'info'
			data['heading'] = 'Info'
			return render_to_response('student/guide.html', data)
	except:
		pass
	return redirect('/student/login')

def dashboard(request, message_status=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			query = Student.objects.get(id=student_id)
			team = Team.objects.filter(student__id=student_id)
			team_confirmed = Team.objects.filter(student__id=student_id, status='confirmed')
			team_leaved = Team.objects.filter(student__id=student_id)
			if len(team) != 0:
				member = Student.objects.filter(team__name=team[0].name, team__status='confirmed')
				member_pending = Student.objects.filter(team__name=team[0].name, team__status='pending')
			else:
				member = Student.objects.none()
				member_pending = Student.objects.none()
			print len(member_pending)
			print len(team_confirmed)

			data =  {	'query':query,
						'team':team,
						'team_confirmed':team_confirmed,
						'member':member,
						'member_pending':member_pending,
						'title_tag':'ENSIGN | Dashboard'
					}
			data['message'] = "['ENSIGN | Dashboard', 'Manage Account and Team.']"
			data['icon'] = 'info'
			data['heading'] = 'Info'
			data.update(csrf(request))
			if message_status == '0':
				data['message'] = "Nope, be nice people!"
			elif message_status == '1':
				data['message'] = "['ENSIGN | Dashboard','Team successfuly created']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '2':
				data['message'] = "['ENSIGN | Dashboard','Team successfuly updated']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '3':
				data['message'] = "['ENSIGN | Dashboard','Team successfuly deleted']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '4':
				data['message'] = "['ENSIGN | Dashboard','Team successfuly joined']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '5':
				data['message'] = "['ENSIGN | Dashboard','Error: There is no team has appropriate with your invitation code!']"
				data['icon'] = 'error'
				data['heading'] = 'Error'
			elif message_status == '6':
				data['message'] = "['ENSIGN | Dashboard','New team member successfuly confirmed']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '7':
				data['message'] = "['ENSIGN | Dashboard','Your team membership request has been cancelled']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '8':
				data['message'] = "['ENSIGN | Dashboard','Account information successfuly updated']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '9':
				data['message'] = "['ENSIGN | Dashboard','Please use digits only to fill in this form (student identity card number).']"
				data['icon'] = 'error'
				data['heading'] = 'Error'
			elif message_status == '10':
				data['message'] = "['ENSIGN | Dashboard','Please use ascii letters plus space charachter only to fill in this form (full name).']"
				data['icon'] = 'error'
				data['heading'] = 'Error'
			return render_to_response('student/dashboard.html', data)
	except:
		pass
	return redirect('/student/login')

def dashboard_update(request, ID):
	try:
		if request.session['Student_id']:
			item = Student.objects.get(id=ID)
			item.fullname = request.POST['fullname']
			if not fullnameval(item.fullname):
				return redirect('/student/dashboard/10')
			item.sicnumber = request.POST['sicnumber']
			if not numval(item.sicnumber):
				return redirect('/student/dashboard/9')
			item.save()
			return redirect('/student/dashboard/8')
	except:
		pass
	return redirect('/student/login')

def problem(request, message_status=''):
	try:
		if request.session['Student_id']:

			# check team and add writeup and solve.
			T = Team.objects.all()
			for t in T:
				if len(Writeup.objects.filter(team__name=t.name)) == 0 and len(Solve.objects.filter(team__name=t.name)) == 0:
					team = t
					for problem in Problem.objects.all():
						date_created = datetime.datetime.now()
						Writeup(
							problem=problem,
							team=team,
							date_created=date_created).save(force_insert=True)
						Solve(
							problem=problem,
							team=team,
							date_created=date_created).save(force_insert=True)

			student_id = request.session['Student_id']
			team = Team.objects.filter(student__id=student_id)
			if len(team) == 1:

				unsolved = Solve.objects.filter(team__id=team[0].id)
				problem = Problem.objects.all()
				data = {	
							'problem': problem,
							'query': unsolved,
							'title_tag': 'ENSIGN | Problem'
						}
				data.update(csrf(request))
				if message_status == '1':
					data['message'] = "['Team successfuly created']"
				elif message_status == '2':
					data['message'] = "['Team successfuly updated']"
				elif message_status == '3':
					data['message'] = "['Team successfuly deleted']"
				else:
					data['message'] = "['ENSIGN | Problem', 'Are you ready to solve all problems?']"
				data['icon'] = 'info'
				data['heading'] = 'Info'
				return render_to_response('student/problem.html', data)
			else:
				data =  {	
							'title_tag': 'Problem | Student | ENSIGN'
						}
				return render_to_response('student/problem_error.html', data)
	except:
		pass
	return redirect('/student/login')

def workspace(request, problem_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			problem = Problem.objects.get(id=problem_id)
			team = Team.objects.filter(student__id=student_id)[0]
			writeup = Writeup.objects.filter(problem__id=problem_id,team__id=team.id)
			solve = Solve.objects.filter(problem__id=problem_id,team__id=team.id)
			try:
				if len(writeup) == 0 and len(solve) == 0:
					date_created = datetime.datetime.now()
					Writeup(
						problem=problem,
						team=team,
						date_created=date_created).save(force_insert=True)
					Solve(
						problem=problem,
						team=team,
						date_created=date_created).save(force_insert=True)
			except:
				pass
			
			writeup = Writeup.objects.filter(problem__id=problem_id, team__id=team.id)
			support = Support.objects.filter(problem__id=problem_id)
			evaluation = Evaluation.objects.filter(problem__id=problem_id)
			print 'DEBUG2'

			evsolvnew = []
			evaluationnew = []
			for E in evaluation:
				evsolv = Evsolv.objects.filter(team__name=team.name, evaluation__id=E.id)
				if len(evsolv) == 0:
					evaluationnew.append({'status': False, 'attempt': False, 'picture':E.picture, 'question':E.question, 'A':E.A, 'B':E.B, 'C':E.C, 'D':E.D, 'E':E.E, 'answer':E.answer, 'id':E.id})
				else:
					evsolv = evsolv[0]
					evaluationnew.append({'status': evsolv.status, 'attempt': evsolv.attempt, 'picture':E.picture, 'question':E.question, 'A':E.A, 'B':E.B, 'C':E.C, 'D':E.D, 'E':E.E, 'answer':E.answer, 'id':E.id})

			print evsolvnew
			print evaluationnew

			newsupport = []
			for sprt in support:
				newsupport.append({'title': sprt.title, 'post': bbcodetohtml(sprt.post)})

			try:
				writeup = writeup[0]
			except:
				pass

			data =  {	'problem': problem,
						'writeup': writeup,
						'support': newsupport,
						'evaluation': evaluationnew,
						'title_tag': 'ENSIGN | Workspace'
					}
			return render_to_response('student/workspace.html', data)
	except:
		pass
	return redirect('/student/login')

def workspace_update(request,problem_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			T = Team.objects.filter(student__id=student_id)[0]
			P = Problem.objects.get(id=problem_id)
			WRITEUP = Writeup.objects.filter(team__name=T.name, problem__id=P.id)
			for W in WRITEUP:
				W.known_list = request.GET['known_list']
				W.unknown_list = request.GET['unknown_list']
				W.todo_list = request.GET['todo_list']
				W.problem_statement = request.GET['problem_statement']
				W.conclusion = request.GET['conclusion']
				W.date_created = datetime.datetime.now()
				W.save()
			return HttpResponse("True")
	except:
		pass
	return redirect('/student/login')

"""
siswa menjawab pertanyaan evaluasi
request yang dikirimkan adalah jawaban dan id pertanyaan.
trus ada update otomatis.
jika benar
	maka poin ditambahkan ke tim (10 poin).
	kemudian siswa dimasukan ke dalam log database penyelesai evaluasi.
	kemudian status dinonaktifkan agar siswa lain dalam satu tim tidak usah menjawab lagi.
	
"""
def evaluation_check_answer(request):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			eval_id = request.GET['eval_id']
			answer = request.GET['answer']
			
			T = Team.objects.filter(student__id=student_id)[0]
			E = Evaluation.objects.get(id=eval_id)
			date_created = datetime.datetime.now()
			print len(Evsolv.objects.filter(team__name=T.name, evaluation__id=E.id))
			if len(Evsolv.objects.filter(team__name=T.name, evaluation__id=E.id)) == 0:
				Evsolv(
					status=False,
					attempt=False,
					team=T,
					evaluation=E,
					date_created=date_created).save(force_insert=True)

			evsolv = Evsolv.objects.filter(team__name=T.name, evaluation__id=E.id)[0]
			print evsolv.attempt, evsolv.status
			if evsolv.attempt == False:
				if evsolv.status == False:
					if E.answer == answer:
						T.point = T.point + E.point
						T.save()
						evsolv.status = True
						evsolv.attempt = True
						evsolv.save()
						return HttpResponse("True")
					else:
						evsolv.attempt = True
						evsolv.save()
						return HttpResponse("False")
			else:
				if evsolv.status == True:
					return HttpResponse("Your team already solve this evaluation.")
				else:
					return HttpResponse("Sorry, only one attempt.")
	except:
		pass
	return redirect('/student/login')

def check_answer(request):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			problem_id = request.GET['problem_id']

			team = Team.objects.filter(student__id=student_id)[0]
			solve = Solve.objects.filter(problem__id=problem_id,team__id=team.id)[0]
			writeup = Writeup.objects.filter(problem__id=problem_id,team__id=team.id)[0]
			if solve.status == False:
				answer = request.GET['answer']
				P = Problem.objects.get(id=problem_id)
				if P.flag == answer:
					T = Team.objects.filter(student__id=student_id)[0]
					T.point = T.point + P.point
					T.save()
					solve.status = True
					solve.save()
					writeup.answer = answer
					writeup.save()
					return HttpResponse("True")
				solve.tries = solve.tries + 1
				solve.save()
			else:
				return HttpResponse("You already solve this problem.")
			return HttpResponse("False")
	except:
		pass
	return redirect('/student/login')

def team(request, message_status=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			team = Team.objects.filter(student__id=student_id)
			if len(team) == 0:
				data =  {
							'title_tag':'Team | Student | ENSIGN',
						}
				data.update(csrf(request))
				if message_status == '1':
					data['message'] = 'Team successfuly created'
				elif message_status == '2':
					data['message'] = 'Team successfuly updated'
				elif message_status == '3':
					data['message'] = 'Team successfuly leaved'
				elif message_status == '4':
					data['message'] = 'Invitation code has been taken. Try Again!'
				elif message_status == '5':
					data['message'] = 'Team name has been taken. Try Again!'
					data['icon'] = 'error'
					data['heading'] = 'Error'
				return render_to_response('student/team.html', data)
			else:
				data =  {
							'title_tag':'Team | Student | ENSIGN'
						}
				return render_to_response('student/team_error.html', data)
	except:
		pass
	return redirect('/student/login')

def team_create(request):
	try:
		if request.session['Student_id']:
			invitation_code = generate_invitation_code()
			team = Team.objects.filter(invitation_code=invitation_code)
			if len(team) == 0:
				name = request.POST['name']
				description = request.POST['description']
				date_created = datetime.datetime.now()
				ID = request.session['Student_id']
				S = Student.objects.get(id=ID)
				if len(Team.objects.filter(name=name)) != 0:
					return redirect('/student/team/5')
				else:
					Team(
						student=S,
						name=name, 
						description=description,
						invitation_code=invitation_code,
						date_created=date_created).save(force_insert=True)
				return redirect('/student/dashboard/1')
			else:
				return redirect('/student/team/4')
	except:
		pass
	return redirect('/student/login')

def team_update(request, ID=''):
	try:
		if request.session['Student_id']:
			item = Team.objects.get(id=ID)
			data =  {	'item':item,
						'title_tag': 'Update | Team | Teacher | ENSIGN'
					}
			data.update(csrf(request))
			return render_to_response('student/team_update.html', data)
	except:
		pass
	return redirect('/student/login')

def team_update_process(request, team_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			S = Student.objects.get(id=student_id)
			T = Team.objects.get(id=team_id)
			T.description = request.POST['description']
			T.student = S
			T.save()
			return redirect('/student/dashboard/2')
	except:
		pass
	return redirect('/student/login')

def team_leave_process(request, team_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			team = Team.objects.filter(id=team_id, student__id=student_id)
			return redirect('/student/dashboard/3')
	except:
		pass
	return redirect('/student/login')

def team_join(request):
	try:
		if request.session['Student_id']:
			invitation_code = request.POST['invitation_code']
			existing_team = Team.objects.filter(invitation_code=invitation_code)
			if len(existing_team) > 0 and len(existing_team) < 3:
				existing_team = existing_team[0]
				student_id = request.session['Student_id']
				S = Student.objects.get(id=student_id)
				Team(
					student=S,
					status='pending',
					name=existing_team.name, 
					description=existing_team.description,
					invitation_code=existing_team.invitation_code,
					point=existing_team.point,
					date_created=existing_team.date_created).save(force_insert=True)
				return redirect('/student/dashboard/4')
			else:
				return redirect('/student/dashboard/5')
	except:
		pass
	return redirect('/student/login')

def team_confirm_process(request, member_pending_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			team = Team.objects.filter(student__id=member_pending_id)[0]
			team.status = 'confirmed'
			team.save()
			return redirect('/student/dashboard/6')
	except:
		pass
	return redirect('/student/login')

def team_cancel_process(request, team_id=''):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			try:
				Team.objects.filter(id=team_id, student__id=student_id).delete()
				return redirect('/student/dashboard/7')
			except:
				return redirect('/student/dashboard/0')
	except:
		pass
	return redirect('/student/login')

"""
agregasi: 
	w - tp, ap 
	p - mp, ep 
""" 
def scoreboard(request):
	try:
		if request.session['Student_id']:
			try:
				# mengenumerasi tim
				uniqteam = []
				for t in Team.objects.all():
					if t.name not in uniqteam:
						uniqteam.append(t.name)
				print uniqteam

				# write up point
				"""
				{'team':[point]}
				"""
				wpoint = {}
				print '\n[+] Write Up | Point'
				W = Writeup.objects.all()
				W = W.order_by('team__name')
				for t in uniqteam:
					pts = []
					for w in W:
						if t == w.team.name:
							# print t, w.point, w.teacher_point
							if w.point != '':
								pts.append(int(w.point))
							if w.teacher_point != '':
								pts.append(int(w.teacher_point))
					wpoint[t] = sum(pts)
				print wpoint

				team = Team.objects.order_by('point').reverse()
				
				TN = []
				TP = []

				for T in team:
					if T.name not in TN:
						TN.append(T.name)
						TP.append(T.point + wpoint[T.name])
				print T.name

				TP, TN = zip(*sorted(zip(TP, TN)))
				
				Point = [x for x in TP]
				Names = [x for x in TN]
				Point.reverse()
				Names.reverse()

				rank = []
				for tn, tp in zip(Names, Point):
					try:
						ts = Team.objects.get(name=tn)
						tssf = ts.student.fullname
						ddd = {'name': tn, 'point': tp, 'student':u"{}".format(tssf)}
						rank.append(ddd)
						print len(rank)
					except:
						pass

				print len(rank)
				data =  {	'team': rank,
							'title_tag': 'ENSIGN | Scoreboard'
						}
				data['message'] = "['ENSIGN | Scoreboard', 'Celebrate your work!']"
				data['icon'] = 'info'
				data['heading'] = 'Info'

				data.update(csrf(request))
			except:
				data = {'title_tag': 'ENSIGN | Scoreboard'}
				writeup = []
				if not writeup:
					data['message'] = "['Scoreboard is still blank.', 'Your student yet solved the problem!']"
					data['icon'] = 'warning'
					data['heading'] = 'Warning'
			return render_to_response('student/scoreboard.html', data)
	except:
		pass
	return redirect('/student/login')

def statistic(request):
	try:
		if request.session['Student_id']:
			student_id = request.session['Student_id']
			team = Team.objects.filter(student__id=student_id)
			if len(team) == 1:
				team = team[0]
				solve = Solve.objects.filter(team__id=team.id)
				
				solved = Solve.objects.filter(team__id=team.id, status=True)
				unsolved = Solve.objects.filter(team__id=team.id, status=False)

				data =  {	'solve': solve,
							'title_tag': 'ENSIGN | Statistic'
						}
				data['message'] = "['ENSIGN | Statistic', 'Review your performance.']"
				data['icon'] = 'info'
				data['heading'] = 'Info'
				data.update(csrf(request))
				data['solved'] = len(solved)
				data['unsolved'] = len(unsolved)
				return render_to_response('student/statistic.html', data)
			else:
				data =  {	
							'title_tag': 'ENSIGN | Statistic'
						}
				return render_to_response('student/statistic_error.html', data)
	except:
		pass
	return redirect('/student/login')

def logout(request):
	try:
		del request.session['Student_id']
	except KeyError:
		pass
	return redirect('/student/')

def signup_form(request, message=''):
	if message == '0':
		message = 'Sorry, username has been taken.'
		color = 'alert'
		icon = 'x-circle'
	elif message == '1':
		message = 'Thank you for registering in our system. Please Log in.'
		color = 'success'
		icon = 'check'
	elif message == '2':
		message = 'Please use at least 8 charachters to fill in this form (password).'
		color = 'alert'
		icon = 'x-circle'
	elif message == '3':
		message = 'Please use letters only to fill in this form (full name).'
		color = 'alert'
		icon = 'x-circle'
	elif message == '4':
		message = 'Please use digits only to fill in this form (student identity card number).'
		color = 'alert'
		icon = 'x-circle'
	else:
		message = False
		color = False
		icon = False
	data = {'title_tag':'ENSIGN | Sign Up'}
	data['message'] = message
	data['color'] = color
	data['icon'] = icon
	data.update(csrf(request))
	return render_to_response('student/signup.html', data)

def signup(request):
	try:		
		username = request.POST.get('username')
		password = request.POST.get('password')
		print username, password
		if len(password) < 8:
			return redirect('/student/signup/form/2')
		fullname = request.POST.get('fullname')
		charset = string.ascii_letters + " " + "'"
		for char in fullname:
			if char not in charset:
				return redirect('/student/signup/form/3')
		sicnumber = request.POST.get('sicnumber')
		for char in sicnumber:
			if char not in string.digits:
				return redirect('/student/signup/form/4')
		date_created = datetime.datetime.now()
		print sicnumber
		password, salt = password_hashing(password, os.urandom(16))
		print password, salt
		S = Student.objects.filter(username=username)
		print S
		if len(S) != 0:
			return redirect('/student/signup/form/0')
		else:
			Student(username=username, password=password, salt=salt, fullname=fullname, sicnumber=sicnumber, date_created=date_created).save()
			return redirect('/student/signup/form/1')
	except:
		pass
	return redirect('/student/signup/form/0')	

def frontend_test(request):
	data =  {	
				'title_tag': 'ENSIGN | Test'
			}
	return render_to_response('index.html', data)
