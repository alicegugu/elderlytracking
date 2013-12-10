from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
# Create your views here.
def hello_template(request):
	name = "mike"
	t = get_template('hello.html')
	html = t.render(Context({'name' : name}))
	return HttpResponse(html)