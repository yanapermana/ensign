from django.conf.urls import patterns, url

urlpatterns = patterns('teacher.views',
	url(r'^$','index'),
	url(r'^about$','about'),
	url(r'^login$','login'),
	url(r'^login/error','login_error'),
	url(r'^logout$','logout'),
	url(r'^dashboard/([\d]+)','dashboard'),
	url(r'^dashboard$','dashboard'),
	url(r'^dashboard/update/([\d]+)','dashboard_update'),
	url(r'^problem/([\d]+)','problem'),
	url(r'^problem$','problem'),
	url(r'^problem/create$','problem_create'),
	url(r'^problem/update/([\d]+)','problem_update'),
	url(r'^problem/update/process/([\d]+)','problem_update_process'),
	url(r'^problem/delete/process/([\d]+)','problem_delete_process'),
	url(r'^problem/evaluation/([\d]+)/([\d]+)','evaluation'),
	url(r'^problem/evaluation/([\d]+)','evaluation'),
	url(r'^problem/evaluation/create$','evaluation_create'),
	url(r'^problem/evaluation/update/([\d]+)/([\d]+)','evaluation_update'),
	url(r'^problem/evaluation/update/process/([\d]+)','evaluation_update_process'),
	url(r'^problem/evaluation/delete/process/([\d]+)/([\d]+)','evaluation_delete_process'),
	url(r'^problem/support/([\d]+)/([\d]+)','support'),
	url(r'^problem/support/([\d]+)','support'),
	url(r'^problem/support/create$','support_create'),
	url(r'^problem/support/update/([\d]+)/([\d]+)','support_update'),
	url(r'^problem/support/update/process/([\d]+)','support_update_process'),
	url(r'^problem/support/delete/process/([\d]+)/([\d]+)','support_delete_process'),
	url(r'^scoreboard$','scoreboard'),
	url(r'^statistic$','statistic'),
	url(r'^writeup$','writeup'),
	url(r'^writeup/update$','writeup_update'),
	url(r'^writeup/search$','writeup_search'),
	url(r'^frontend$','frontend'),
)