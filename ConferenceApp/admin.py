from django.contrib import admin
from django.contrib import admin
from .models import conference,submission
# Register your models here.
admin.site.register(conference)
admin.site.register(submission)
admin.site.site_header = "Conference Management"
admin.site.site_title = "Conference Admin Portal"
admin.site.index_title = "Welcome to the Conference Admin Portal"
