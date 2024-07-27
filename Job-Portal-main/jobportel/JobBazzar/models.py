from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm


class Job(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')  # Assuming you're storing logos as image files
    location = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100,null=True,blank=True)
    current_date = models.DateField(auto_now_add=True)
    hours = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    job_description = models.TextField()
    key_responsibilities = models.TextField()
    skill = models.TextField()
    skill1 = models.CharField(max_length=100,null=True,blank=True)
    skill2 = models.CharField(max_length=100,null=True,blank=True)
    skill3 = models.CharField(max_length=100,null=True,blank=True)
    experience = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    need = models.CharField(max_length=100)
    id = models.CharField(max_length=50,primary_key=True,editable=False)
    emails = models.CharField(max_length=100)

class Profile(models.Model):
    email = models.EmailField(primary_key=True);
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    # email = models.EmailField()
    school = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    age = models.CharField(max_length=5)
    experience = models.CharField(max_length=100)
    experience_field = models.CharField(max_length=500,null=True,blank=True)
    passingYear = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    cgpa = models.CharField(max_length=10)
    skills = models.CharField(max_length=255)
    education = models.CharField(max_length=255,null=True,blank=True)
    projects = models.CharField(max_length=400,null=True,blank=True)
    achievements = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

class Company(models.Model):
        email = models.EmailField()
        company_name = models.CharField(max_length=100,primary_key=True)
        founded = models.CharField(max_length=10)
        phone = models.CharField(max_length=20)
        location = models.CharField(max_length=40)
        primary_industry = models.CharField(max_length=30)
        website = models.CharField(max_length=500)
        password = models.CharField(max_length=1000)
        logo = models.ImageField(upload_to='logos/')

class Application(models.Model):
       name = models.CharField(max_length=30)
       applicant_email = models.EmailField()
       company_email = models.EmailField()
       date = models.DateField(auto_now_add=True)
       status = models.CharField(max_length=40,default='Pending')
       job_id = models.CharField(max_length=30)
       interview = models.CharField(max_length=40)
       job_title = models.CharField(max_length=80)
       cv = models.ImageField(upload_to='CV/')
       id = models.CharField(max_length=30,primary_key=True)
       company= models.CharField(max_length=80,null=True, blank=True)
#        file = models.BinaryField()











def __str__(self):
        return self.job_title
    
def __str__(self):
        return self.email

def __str__(self):
        return self.company_name
def __str__(self):
        return self.id

# Create your models here.
# class UserData(models.Model):
#     # id = models.AutoField,
#     email = models.CharField(max_length=100),
#     fullname =  models.CharField(max_length=100),