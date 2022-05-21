from django.contrib import admin

# Register your models here.
from instapp.models import *
admin.site.register(Pid)
admin.site.register(Manual)
admin.site.register(TwoWire)
admin.site.register(Inst)
admin.site.register(Datasheet)


