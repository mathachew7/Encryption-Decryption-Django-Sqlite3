from django.contrib import admin
from .models import User
from .models import Encrypted_data
# Register your models here.

admin.site.register(User)
admin.site.register(Encrypted_data)
