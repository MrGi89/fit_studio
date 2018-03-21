from django.contrib import admin

from .models import Member, Class, Trainer, Pass

admin.site.register(Member)
admin.site.register(Class)
admin.site.register(Trainer)
admin.site.register(Pass)
