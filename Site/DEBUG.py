import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site.settings')
django.setup()


from Users.models import *
from SolveGia.models import *


User = CustomUser

for t in Task.objects.all():
    print(t.answer)
