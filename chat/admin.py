from django.contrib import admin
from .models import *

from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Appointment)
admin.site.register(AppointmentSlot)
admin.site.register(Profile)

admin.site.register(MentalHealthCondition)