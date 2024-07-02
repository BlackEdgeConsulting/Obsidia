from django.contrib import admin

# Register your models here.
from .models import CaseFile, Organization, TargetOfInterest

admin.site.register(Organization)
admin.site.register(CaseFile)
admin.site.register(TargetOfInterest)
# admin.site.register(Tag)