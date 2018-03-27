from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse
from teacher.models import Teacher, Problem, Evaluation, Support
from student.models import Team, Solve, Writeup
from teacher.defs import bbcodetohtml, BMSearch

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

import datetime
import random

def index(request):
	data = {'title_tag':'ENSIGN | Login'}
	data.update(csrf(request))
	return render_to_response('teacher/login.html', data)

def about(request):
	data = {'title_tag':'ENSIGN | About'}
	return render_to_response('teacher/about.html', data)

def login_error(request):
	data = {'title_tag':'ENSIGN | Login Error'}
	data.update(csrf(request))
	return render_to_response('teacher/login_error.html', data)
	
def login(request):
	try:		
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		auth = Teacher.objects.filter(username__exact=username, password__exact=password)
		if auth[0].username == username and auth[0].password == password :
			request.session['Teacher_id'] = auth[0].id
			return redirect('/teacher/dashboard')
	except:
		pass
	return redirect('/teacher/login/error')

def dashboard(request, message_status=''):
	try:
		if request.session['Teacher_id']:
			ID = request.session['Teacher_id']
			query = Teacher.objects.get(id=ID)
			data = {'query':query}
			data.update(csrf(request))
			data['title_tag'] = 'ENSIGN | Dashboard'
			if message_status == '0':
				data['message'] = "Nope, be nice people!"
			elif message_status == '1':
				data['message'] = 'Account successfuly updated'
				data['icon'] = 'success'
				data['heading'] = 'Success'
			return render_to_response('teacher/dashboard.html', data)
	except:
		pass
	return redirect('/teacher/login')

def dashboard_update(request, ID):
	try:
		if request.session['Teacher_id']:
			item = Teacher.objects.get(id=ID)
			item.fullname = request.POST['fullname']
			item.ticnumber = request.POST['ticnumber']
			item.save()
			return redirect('/teacher/dashboard/1')
	except:
		pass
	return redirect('/teacher/login')
			

def problem(request, message_status=''):
	try:
		if request.session['Teacher_id']:
			query = Problem.objects.all().order_by('-date_created')
			data = {'query':query}
			for item in query:
				print item.limited_questions.encode('hex')
			data['title_tag'] = 'ENSIGN | Problem'
			data.update(csrf(request))
			if message_status == '1':
				data['message'] = "['Problem successfuly created']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '2':
				data['message'] = "['Problem successfuly updated']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '3':
				data['message'] = "['Problem successfuly deleted']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			if not query:
				data['message'] = "['Problem is still blank.', 'Do not forget to make a new problem!']"
				data['icon'] = 'warning'
				data['heading'] = 'Warning'
			return render_to_response('teacher/problem.html', data)
	except:
		pass
	return redirect('/teacher/login')

def problem_create(request):
	try:
		if request.session['Teacher_id']:
			teacher_id = request.session['Teacher_id']
			T = Teacher.objects.get(id=teacher_id)
			title = request.POST['title']
			description = request.POST['description']
			limited_questions = request.POST['limited_questions']
			keyword = request.POST['keyword']
			flag = request.POST['flag']
			point = request.POST['point']
			try: attachment = request.FILES['attachment']
			except: pass
			try: picture = request.FILES['picture']
			except: pass
			date_created = datetime.datetime.now()
			Problem(
				teacher=T,
				title=title, 
				description=description,
				limited_questions=limited_questions,
				keyword=keyword,
				flag=flag,
				point=point,
				attachment=attachment,
				picture=picture,
				date_created=date_created).save(force_insert=True)

			# add solve and writeup
			problem = Problem.objects.get(title=title)
			for team in Team.objects.all():
				Writeup(
					problem=problem,
					team=team,
					date_created=date_created).save(force_insert=True)
				Solve(
					problem=problem,
					team=team,
					date_created=date_created).save(force_insert=True)
			return redirect('/teacher/problem/1')
	except:
		pass
	return redirect('/teacher/login')

def problem_update(request, ID=''):
	try:
		if request.session['Teacher_id']:
			item = Problem.objects.get(id=ID)
			data = {'item':item}
			data.update(csrf(request))
			data['title_tag'] = 'Update | Problem | Teacher | ENSIGN'
			return render_to_response('teacher/problem_update.html', data)
	except:
		pass
	return redirect('/teacher/login')

def problem_update_process(request, ID=''):
	try:
		if request.session['Teacher_id']:
			P = Problem.objects.get(id=ID)
			P.title = request.POST['title']
			P.description = request.POST['description']
			limited_questions = request.POST['limited_questions']
			limited_questions = limited_questions.replace('\t','')
			limited_questions = limited_questions.replace('\r\n\r\n','\r\n')
			limited_questions = limited_questions.replace('\n\n','\n')
			limited_questions = limited_questions.replace('\r\n','\n')
			limited_questions = limited_questions.rstrip()
			# print limited_questions.encode('hex')
			P.limited_questions = limited_questions
			P.keyword = request.POST['keyword']
			P.flag = request.POST['flag']
			P.point = request.POST['point']

			try: P.attachment = request.FILES['attachment']
			except: pass
			try: P.picture = request.FILES['picture']
			except: pass
			
			teacher_id = request.session['Teacher_id']
			T = Teacher.objects.get(id=teacher_id)
			P.teacher = T
			P.save()
			return redirect('/teacher/problem/2')
	except:
		pass
	return redirect('/teacher/login')

def problem_delete_process(request, problem_id=''):
	try:
		if request.session['Teacher_id']:
			Problem.objects.filter(id=problem_id).delete()
			return redirect('/teacher/problem/3')
	except:
		pass
	return redirect('/teacher/login')

def evaluation(request, problem_id='', message_status=''):
	try:
		if request.session['Teacher_id']:
			query = Evaluation.objects.filter(problem__id=problem_id)
			data  = {	'query':query, 
						'problem_id':problem_id,
						'title_tag':'ENSIGN | Evaluation'	
					}
			data.update(csrf(request))
			if message_status == '1':
				data['message'] = "['Evaluation successfuly created']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '2':
				data['message'] = "['Evaluation successfuly updated']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '3':
				data['message'] = "['Evaluation successfuly deleted']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			if not query:
				data['message'] = "['Evaluation is still blank.', 'Do not forget to make a new evaluation!']"
				data['icon'] = 'warning'
				data['heading'] = 'Warning'
			return render_to_response('teacher/evaluation.html', data)
	except:
		pass
	return redirect('/teacher/login')

def evaluation_create(request):
	try:
		if request.session['Teacher_id']:
			question = request.POST['question']
			A = request.POST['A']
			B = request.POST['B']
			C = request.POST['C']
			D = request.POST['D']
			E = request.POST['E']
			answer = request.POST['answer']
			point = request.POST['point']
			difficult_level = request.POST['difficult_level']
			difficult_forecast = request.POST['difficult_forecast']
			date_created = datetime.datetime.now()
			problem_id = request.POST['problem_id']
			P = Problem.objects.get(id=problem_id)

			try: 
				picture = request.FILES['picture']
				Evaluation(
					problem=P,
					question=question, 
					picture=picture,
					A=A,
					B=B,
					C=C,
					D=D,
					E=E,
					answer=answer,
					point=point,
					difficult_level=difficult_level,
					difficult_forecast=difficult_forecast,
					date_created=date_created).save(force_insert=True)
			except: 
				Evaluation(
					problem=P,
					question=question, 
					A=A,
					B=B,
					C=C,
					D=D,
					E=E,
					answer=answer,
					point=point,
					difficult_level=difficult_level,
					difficult_forecast=difficult_forecast,
					date_created=date_created).save(force_insert=True)
			return redirect('/teacher/problem/evaluation/{0}/1'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

def evaluation_update(request, problem_id='', evaluation_id=''):
	try:
		if request.session['Teacher_id']:
			item = Evaluation.objects.filter(problem__id=problem_id, id=evaluation_id)[0]
			data =  {	'item':item,
						'problem_id':problem_id,
						'title_tag':'Update | Evaluation | Problem | Teacher | ENSIGN'
					}
			data.update(csrf(request))
			return render_to_response('teacher/evaluation_update.html', data)
	except:
		pass
	return redirect('/teacher/login')

def evaluation_update_process(request, evaluation_id):
	try:
		if request.session['Teacher_id']:
			problem_id = request.POST['problem_id']
			E = Evaluation.objects.filter(problem__id=problem_id, id=evaluation_id)[0]
			E.question = request.POST['question']
			E.A = request.POST['A']
			E.B = request.POST['B']
			E.C = request.POST['C']
			E.D = request.POST['D']
			E.E = request.POST['E']
			E.answer = request.POST['answer']
			E.point = request.POST['point']
			E.difficult_level = request.POST['difficult_level']
			E.difficult_forecast = request.POST['difficult_forecast']
			P = Problem.objects.get(id=problem_id)
			E.problem = P
			try: 
				E.picture = request.FILES['picture']
			except:
				pass
			E.save()
			return redirect('/teacher/problem/evaluation/{0}/2'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

def evaluation_delete_process(request, problem_id='', evaluation_id=''):
	try:
		if request.session['Teacher_id']:
			E = Evaluation.objects.filter(problem__id=problem_id, id=evaluation_id)
			E.delete()
			return redirect('/teacher/problem/evaluation/{0}/3'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

def support(request, problem_id='', message_status=''):
	try:
		if request.session['Teacher_id']:
			query = Support.objects.filter(problem__id=problem_id)
			data  = {	
						'problem_id':problem_id,
						'title_tag':'ENSIGN | Support'	
					}
			
			stitle = []
			spost = []
			sid = []

			for S in query:
				stitle.append(S.title)
				spost.append(S.post)
				sid.append(S.id)

			stitle.reverse()
			spost.reverse()
			sid.reverse()

			snew = []
			tohtml = ''			
			for st, sp, si in zip(stitle, spost, sid):
				tohtml = bbcodetohtml(sp)
				snew.append({'title': st, 'post': tohtml, 'id': si})

			data.update(csrf(request))
			if message_status == '1':
				data['message'] = "['Support successfuly created']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '2':
				data['message'] = "['Support successfuly updated']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			elif message_status == '3':
				data['message'] = "['Support successfuly deleted']"
				data['icon'] = 'success'
				data['heading'] = 'Success'
			if not query:
				data['message'] = "['Support is still blank.', 'Do not forget to make a new support!']"
				data['icon'] = 'warning'
				data['heading'] = 'Warning'
			data['query'] = snew
			return render_to_response('teacher/support.html', data)
	except:
		pass
	return redirect('/teacher/login')

def support_create(request):
	try:
		if request.session['Teacher_id']:
			title = request.POST['title']
			post = request.POST['post']
			date_created = datetime.datetime.now()
			problem_id = request.POST['problem_id']
			P = Problem.objects.get(id=problem_id)
			Support(
				problem=P,
				title=title, 
				post=post,
				date_created=date_created).save(force_insert=True)
			return redirect('/teacher/problem/support/{0}/1'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

def support_update(request, problem_id='', support_id=''):
	try:
		if request.session['Teacher_id']:
			item = Support.objects.get(problem=problem_id, id=support_id)
			data =  {	'item':item,
						'problem_id':problem_id,
						'title_tag':'ENSIGN | Support'
					}
			data.update(csrf(request))
			return render_to_response('teacher/support_update.html', data)
	except:
		pass
	return redirect('/teacher/login')

def support_update_process(request, support_id=''):
	try:
		if request.session['Teacher_id']:
			problem_id = request.POST['problem_id']
			E = Support.objects.filter(problem__id=problem_id, id=support_id)[0]
			print 'DEBUG1'
			E.title = request.POST['title']
			E.post = request.POST['post']
			P = Problem.objects.get(id=problem_id)
			print 'DEBUG2'
			E.problem = P
			E.save()
			return redirect('/teacher/problem/support/{0}/2'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

def support_delete_process(request, problem_id='', support_id=''):
	try:
		if request.session['Teacher_id']:
			E = Support.objects.get(problem=problem_id, id=support_id)
			E.delete()
			return redirect('/teacher/problem/support/{0}/3'.format(problem_id))
	except:
		pass
	return redirect('/teacher/login')

"""
agregasi: 
	w - tp, ap 
	p - mp, ep 
""" 
def scoreboard(request):
	try:
		if request.session['Teacher_id']:
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

				data.update(csrf(request))
			except:
				data = {'title_tag': 'ENSIGN | Scoreboard'}
				writeup = []
				if not writeup:
					data['message'] = "['Scoreboard is still blank.', 'Your student yet solved the problem!']"
					data['icon'] = 'warning'
					data['heading'] = 'Warning'
			return render_to_response('teacher/scoreboard.html', data)
	except:
		pass
	return redirect('/teacher/login')

def statistic(request):
	try:
		if request.session['Teacher_id']:
			solve = Solve.objects.all()
			data =  {	'solve': solve,
						'title_tag': 'ENSIGN | Statistics'
					}
			data.update(csrf(request))
			# mengenumerasi nama tim
			uniqteam = []
			for t in Team.objects.all():
				if t.name not in uniqteam:
					uniqteam.append(t.name)
			print uniqteam
			# mengenumerasi judul masalah
			uniqprob = []
			for p in Problem.objects.all():
				if p.title not in uniqprob:
					uniqprob.append(p.title)
			print uniqprob
			# generate triesstats
			triesstats = {}
			for uniqteamitem in uniqteam:
				listtry = [0 for i in uniqprob]
				listtrypluscolor = []
				s = Solve.objects.filter(team__name=uniqteamitem)
				for ss in s:
					listtry[uniqprob.index(ss.problem.title)] = ss.tries
				listtrypluscolor.append( [random.randint(0, 255) for i in xrange(3)] )
				listtrypluscolor.append(listtry)
				triesstats[uniqteamitem] = listtrypluscolor
			data['problem'] = uniqprob
			
			data['stats_tries'] = triesstats
			
			return render_to_response('teacher/statistic.html', data)
	except:
		pass
	return redirect('/teacher/login')


def writeup(request):
	try:
		if request.session['Teacher_id']:
			data = {}
			data['title_tag'] = 'ENSIGN | Write Up'
			W = Writeup.objects.all().order_by('-date_created')

			def rate():
				for w in W:
					if len(w.known_list) > 10:
						content = ''
						content += w.known_list + '\n'
						content += w.unknown_list + '\n'
						content += w.todo_list + '\n'
						content += w.problem_statement + '\n'
						content += w.conclusion + '\n'
						content = content.lower()
						keyword = w.problem.keyword.replace(' ','').split(',')
						point = 0
						for k in keyword:
							try:
								if BMSearch(content.lower(), k.lower()) != -1:
									point += 1;
							except: pass
						try: score = ( float(point) / len(keyword) ) * 100; w.point = score; w.save();
						except: pass
					
			rate()
			W = W.order_by('-date_created')
			paginator = Paginator(W, 10)

			page = request.GET.get('page')
			try:
				Ws = paginator.page(page)
			except PageNotAnInteger:
				Ws = paginator.page(1)
			except EmptyPage:
				Ws = paginator.page(paginator.num_pages)

			data['writeup'] = Ws

			if not Ws:
				data['message'] = "['Write Up is still blank.', 'Your student yet solved the problem!']"
				data['icon'] = 'warning'
				data['heading'] = 'Warning'

			data.update(csrf(request))
			return render_to_response('teacher/writeup.html', data)
	except:
		pass
	return redirect('/teacher/login')

# add teacher point
def writeup_update(request):
	try:
		if request.session['Teacher_id']:
			teacher_id = request.session['Teacher_id']
			wid = request.GET['id']
			wpoint = request.GET['teacher_point']
			W = Writeup.objects.get(id=wid)
			W.teacher_point = wpoint
			W.save()
			return HttpResponse(wpoint)
	except:
		pass
	return redirect('/teacher/login')

def writeup_search(request):
	try:
		if request.session['Teacher_id']:
			keyword = request.POST.get('keyword')
			team_name = keyword.split(':')[0]
			problem_title = keyword.split(':')[1]
			print '[o] team_name: {}'.format(team_name)
			print '[o] problem_title: {}'.format(problem_title)

			W = Writeup.objects.filter(problem__title__contains=problem_title,team__name__contains=team_name)

			def rate():
				for w in W:
					if len(w.known_list) > 10:
						content = ''
						content += w.known_list + '\n'
						content += w.unknown_list + '\n'
						content += w.todo_list + '\n'
						content += w.problem_statement + '\n'
						content += w.conclusion + '\n'
						content = content.lower()
						keyword = w.problem.keyword.replace(' ','').split(',')
						point = 0
						for k in keyword:
							try:
								if BMSearch(content.lower(), k.lower()) != -1:
									point += 1;
							except: pass
						try: score = ( float(point) / len(keyword) ) * 100; w.point = score; w.save();
						except: pass
					
			rate()
			try:
				W = W.order_by('-date_created')
				paginator = Paginator(W, 10)
				page = request.GET.get('page')
			except:
				pass

			try:
				Ws = paginator.page(page)
			except PageNotAnInteger:
				Ws = paginator.page(1)
			except EmptyPage:
				Ws = paginator.page(paginator.num_pages)
			data = {}
			data['writeup'] = Ws

			if not Ws:
				data['message'] = "['Write Up is still blank.', 'Your student yet solved the problem!']"
				data['icon'] = 'warning'
				data['heading'] = 'Warning'
			else:
				data['message'] = "['Write-up available.']"
				data['icon'] = 'success'
				data['heading'] = 'Result'

			data.update(csrf(request))
			return render_to_response('teacher/writeup.html', data)
			# return redirect('/teacher/writeup')
	except:
		pass
	return redirect('/teacher/login')

def logout(request):
	try:
		del request.session['Teacher_id']
	except KeyError:
		pass
	return redirect('/teacher/')

def frontend(request):
	return render_to_response('teacher/basic.html')