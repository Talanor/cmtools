from django.contrib import admin

from .models import Mention, Client

admin.site.register(Mention)
admin.site.register(Client)