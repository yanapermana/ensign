from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.

def handler404(request):
	response = render_to_response('error/404.html',{}, context_instance = RequestContext(request))
	response.status_code = 404
	return response
