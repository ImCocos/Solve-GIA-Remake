import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site.settings')
django.setup()


from Users.models import *
from SolveGia.models import *


User = CustomUser

for t in Task.objects.filter(pk=4483):
    print(
f"""
Task - {t}:
    pk: {t.pk},
    cat: {t.category},
    type_number: {t.type_number},    
    answer" {t.answer},
    photos: {t.photos},
    files: {t.files},
    rating: {t.rating}
    text:\n
{t.text}
""")

# cat = Category(name='Informatika', description='Informatika category')
# cat.save()
