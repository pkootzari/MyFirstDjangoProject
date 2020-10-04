from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Service)
admin.site.register(models.Invoice)
admin.site.register(models.Order)
admin.site.register(models.ContactInfo)
admin.site.register(models.Ticket)
admin.site.register(models.Message)