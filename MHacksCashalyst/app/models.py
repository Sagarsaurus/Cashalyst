from django.db import models
from django.utils.encoding import smart_text

class SignUpInfo(models.Model):
	firstname = models.CharField(max_length = 120, null = True, blank = True)
	lastname = models.CharField(max_length = 120, null = True, blank = True)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	#autonow means that when it updated or changed, it is false. auto now add means only when it is added
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)
	
	def __str__(self):
		return smart_text(self.email)
