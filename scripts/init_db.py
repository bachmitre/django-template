import django
django.setup()

from django.contrib.auth.models import User

"""
Create some initial data 
"""

users = User.objects.all()

if not users:

    print ("Creating superuser admin/admin...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

else:
    print ("Already data in db. Skipping ...")

