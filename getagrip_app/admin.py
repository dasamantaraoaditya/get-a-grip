from django.contrib import admin
from .models import *

admin.site.register(comments_log)
admin.site.register(assignees_log)
admin.site.register(tasks_log)

# Register your models here.
