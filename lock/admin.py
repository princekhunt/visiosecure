from django.contrib import admin
from lock.models import *

# Register your models here.

admin.site.register(Unlockers)

admin.site.register(jobs)

admin.site.register(TAccessCodes)

admin.site.register(RandomFacts)

admin.site.register(TRegistration)

admin.site.register(All_logs)

admin.site.register(access_code)