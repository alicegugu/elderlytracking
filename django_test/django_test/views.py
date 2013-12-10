from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.http import HttpResponse

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)
	
def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')
		
def loggedin(request):
	return render_to_response('loggedin.html', 
							  {'full_name': request.user.username})
							  
							  
def invalid_login(request):
	return render_to_response('invalid.html')
	
def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')
	
def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')
			
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	return render_to_response('register.html',args)

def register_success(request):
	return render_to_response('register_success.html')
	
def register_success(request, position):
	return render_to_response('success.html')
	
def set_position(request):
	cache_key = request.GET.get('tag_id')
	position = request.GET.get('position')
	cache_time = 1800
	cache.set(cache_key, position, cache_time)
	return HttpResponse(cache.get(cache_key))
	