import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trauma.settings')
django.setup()

from api.models import User


def UserAdd():
    try:
        User.objects.create(username = "Nigeb", password="Nigeb@1403",group="lab")
    except:
        print("nashod")
    