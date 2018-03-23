from django.contrib import admin

from .models import Member, Group, Trainer, Pass, Product

admin.site.register(Member)
admin.site.register(Group)
admin.site.register(Trainer)
admin.site.register(Pass)
admin.site.register(Product)
