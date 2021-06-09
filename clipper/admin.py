from django.contrib import admin
from .models import Site, Course, Chapter, Section

admin.site.register(Site)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Section)