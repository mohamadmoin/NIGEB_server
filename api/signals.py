from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Patients

def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='simpleuser')
		instance.groups.add(group)
		# Patients.objects.create(
		# 	user=instance,
		# 	name=instance.username,
		# 	)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)