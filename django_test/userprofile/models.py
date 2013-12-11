from django.db import models
from django.contrib.auth.models import User
from time import time
def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

# Create your models here.
class UserProfile(models.Model):
	user =  models.OneToOneField(User)
	contact_number = models.CharField(max_length=10)
	tag_id = models.CharField(max_length=20)
	layout = models.FileField(upload_to=get_upload_file_name)
	
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])