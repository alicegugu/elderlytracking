from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def user_profile(request):
	if request.method == 'POST' and request.is_ajax():
		form = UserProfileForm(request.POST, request.FILES,instance=request.user.profile)
		if form.is_valid():
			form.save()
			#return HttpResponseRedirect('/accounts/loggedin')
			return HttpResponse("Update success")
		else:
			#return HttpResponseRedirect('/accounts/loggedin')
			return HttpResponse("Update error")
			
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile)
		
	args = {}
	args.update(csrf(request))
	args['form'] = form
	args['full_name'] = request.user.username
	return render_to_response('profile.html', args)

# Create your views here.
