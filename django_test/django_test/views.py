from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pika
import logging
import json


logger = logging.getLogger(__name__)

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

	response_data = {}
	response_data['errors'] = []
	try:
		cache_key = request.GET.get('tag_id')
		position = request.GET.get('position')
		response_data['position'] = position
		response_data['tag_id'] = cache_key

	except Exception, e:
		response_data['errors'].append(e)
	else:
		pass
	finally:
		pass
	
	if cache_key is None:
		response_data['errors'].append('tag id can not be none')
	if position is None:
		response_data['errors'].append('position can not be none')
		pass
	# position will be updated for 30 sec
	cache_time = 30
	cache.set(cache_key, position, cache_time)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def set_gps_position(request):

	response_data = {}
	cache_key = request.GET.get('tag_id')
	position_latitude = request.GET.get('position_latitude')
	position_longitude = request.GET.get('position_longitude')
	
	response_data['errors'] = []
	if cache_key is None:
		response_data['errors'].append('tag id can not be none')

	if position_latitude is None:
		response_data['errors'].append('latitude can not be none')

	if position_longitude is None:
		response_data['errors'].append('longitude can not be none')

	# position will be updated for 30 sec
	cache_time = 30
	cache.set(cache_key+'latitude', position_latitude, cache_time)
	cache.set(cache_key+'longitude', position_longitude, cache_time)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def get_position(request):
	user = request.user
	profile = user.profile
	cache_key = profile.tag_id
	position = cache.get(cache_key)

	response_data = {}
	response_data['position'] = position
	if position is None:
		response_data['status'] = 'lost'

	if cache_key is None:
		response_data['error'] = 'User has no tag attached'
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def indoor_tracking(request):
	user = request.user
	profile = user.profile
	args = {}
	args['layout'] =  profile.layout
	args['full_name'] = request.user.username
	return render_to_response("indoor_tracking.html", args)

@login_required
def outdoor_tracking(request):
	user = request.user
	profile = user.profile
	args = {}
	args['layout'] =  profile.layout
	args['full_name'] = request.user.username
	return render_to_response("outdoor_tracking.html", args)


@login_required
def  alert(request):
	if request.is_ajax():
		response_data = {}
		response_data['errors'] = []
		try:
			connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
			channel = connection.channel()
			channel.queue_declare(queue='alert')

			user = request.user
			profile = user.profile
			contact_number = profile.contact_number
			message = contact_number
			channel.basic_publish(exchange='',
                      routing_key='alert',
                      body=message)
			response_data['message'] = message

		except Exception, e:	
			response_data['errors'].append(e)
		else:
			pass
		finally:
			pass

		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		user = request.user
		profile = user.profile

		args = {}
		args.update(csrf(request))
		args['full_name'] = user.username
		args['contact_number'] = profile.contact_number
		return render_to_response("alert.html", args)


@login_required
def  end_call(request):
	if request.is_ajax():
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='alert')

		message = "end"
		channel.basic_publish(exchange='',
                      routing_key='alert',
                      body=message)

		return HttpResponse("call has been ended")