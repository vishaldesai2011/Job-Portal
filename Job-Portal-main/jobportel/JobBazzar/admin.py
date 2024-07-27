from django.contrib import admin
from .models import Job
from .models import Profile,Company,Application

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    fields = ('id','job_title', 'company_name', 'logo', 'location', 'current_date', 'hours', 'category', 'rate', 'salary', 'job_description', 'key_responsibilities', 'skill', 'experience', 'time', 'job_type', 'need')
    
    
admin.site.register(Job)
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Application)