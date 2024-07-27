from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout 
from .models import Job
from .models import  Profile
from .models import Company
from .models import Application

# from .models import UserData

# For SMTP
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# For Encryption OTP
from django.core.signing import Signer

#for HTML TO PDF
import pdfkit #for Html TO PDF
from django.template.loader import get_template
from django.templatetags.static import static

# Create your views here.
def Home(request):

    # # image_instance = get_object_or_404(Job, logo=param1)
    # url = image_instance.image.url
    # print(f"Download Url{url}")
    first_five_jobs = Job.objects.all()[:8]
    count = len(first_five_jobs)
    li=""
    li_loc = ""
    titles = Job.objects.all()
    name="Login/Register"
    if(request.session.get('userId') != None):
         em = request.session.get('userId')
         data = Profile.objects.get(email=em)
         name = data.name
    else:
         pass
    for i in range(0,count):
         li += titles[i].job_title+"," 
         li_loc += titles[i].location+"," 
    a,t,m,s,g,d,hr,hm,ux,alljob = OpeningPositions()

    return render(request,'JobBazzar/Home.html',{'first_five_jobs':first_five_jobs,'jt':li,'jl':li_loc,"acc":a,"it":t,"me":m,"se":s,"g":g,"da":d,"hr":hr,"hm":hm,"ux":ux,"all":alljob,"name":name})

def OpeningPositions():
     accountent = Job.objects.filter(category="Accountant").count()
     it = Job.objects.filter(category="IT").count()
     me = Job.objects.filter(category="Marketing Executive").count()
     se = Job.objects.filter(category="Sales Executive").count()
     gd = Job.objects.filter(category="Graphic Designer").count()
     da = Job.objects.filter(category="Data Analyst").count()
     hro = Job.objects.filter(category="Human Resources Officer").count()
     hm = Job.objects.filter(category="Hotel Manager").count()
     Uxd = Job.objects.filter(category="UX Designer").count()
     AllJob = Job.objects.all().count()
     return accountent,it,me,se,gd,da,hro,hm,Uxd,AllJob

     




def signin(request):
    print("Sign in Called")
    # print(request.session.get('auth','exp'))
    if request.session.get('auth','exp') == "done":
        
        print("Calling if")
        secret_key = "#007DAP#acbs"
        my_data = request.session.get('id', 'default_value')
        email = decrypt_value(my_data,secret_key)
    # else:
    #     return redirect("Register")
        # return render(request,'JobBazzar/login.html',{'email':email})
        if request.method == 'POST':
            print("Post Calling")
           
            # email1 = request.POST['Email']
            password = request.POST['Password']

            cpassword = request.POST['CPassword']
            if(password == cpassword ) and (len(password) > 8):
                print("Success")
                myuser = User.objects.create_user(email,email,password)
                myuser.save()
                del request.session['auth']
                return redirect('login')
            else:
                messages.error(request,"Password does not match")
                return redirect("signin")

    else:
        # messages.error(request,"Password does not match")
        return redirect("Register")

    
    return render(request,'JobBazzar/login.html',{'email': request.session.get('email', ' ')})


html_content = '<html><body><h1>Hello, World!</h1><p>This is a test email with HTML content.</p></body></html>'
    
def register(request):
    secret_key = "#007DAP#acbs"
    if request.method == 'POST':
    
        ExistUser = username_exists(request.POST['email'])
        print(ExistUser)
        if(ExistUser == False):
                num = str(random.randint(100000, 999999))
                VAL = request.POST.get('email')
                html_content = '<html><body><p>Dear User,<br> <font style="color:#625AA8;font-size:18px;">'+num+'</font> is your one time password(OTP).<br>Please do not share the OTP with others.<br><br>Regards,<br><font style="color:#625AA8;font-size:15px;">Team Job Bazaar</font></p></body></html>'
                send_html_email(settings.EMAIL_HOST_USER,request.POST['email'],"Job Bazaar OTP",html_content,settings.EMAIL_HOST,settings.EMAIL_PORT,"unlockhome07@gmail.com",settings.EMAIL_HOST_PASSWORD)
                value_to_encrypt = num
                encrypted_value= encrypt_value(value_to_encrypt, secret_key)
                MSG = encrypt_value(VAL, secret_key)
                request.session['OTP'] = encrypted_value;
                request.session['id'] = MSG
                request.session['email'] = VAL
                request.session['submit'] = "true";

                return redirect('Verify')
        else:
                messages.error(request,"User already exist")
                return redirect('Register')
            
    return render(request,'JobBazzar/Register.html')

def verify(request):
    print("Verify Calling")
    if request.session.get('submit') is not None and request.session.get('OTP') is not None:
        print("Sessoin  Found")
        if request.method == 'POST':
             print("POST FOUND")
             secret_key = "#007DAP#acbs"
             my_data = request.session.get('OTP', 'default_value')
             print(my_data)
             value = decrypt_value(my_data,secret_key)
             one = request.POST['one']
             two = request.POST['two']
             thr = request.POST['thr']
             fore = request.POST['fou']
             fiv = request.POST['fiv']
             six = request.POST['six']
             otp = one+two+thr+fore+fiv+six
            #  print(otp)
             print("OTP : "+ otp)
             print("VALUE : "+ value)

             if otp == value :
                  del request.session['OTP']
                  del request.session['submit']
                  request.session['auth'] = "done"
                  print("Auth Created")
                  return redirect('signin')
             else:
                 messages.error(request,"Invalid OTP")
    else:
        return redirect('Register')
                #  return HttpResponse("<script>alert('Enter Valid OTP')</script>")
             

            

    return render(request,'JobBazzar/verify.html')

def logins(request):
    if request.method == 'POST':
        uname =  request.POST['email']
        password = request.POST['Password']
        user = authenticate(request, username=uname, password=password)
        if user:
                login(request, user)
                request.session['login'] = "true"   
                request.session['userId'] = uname
                return redirect('Home')
        else:
            messages.error(request,"Invalid Email  or Password")
            return render(request,'JobBazzar/singin.html')
       
    return render(request,'JobBazzar/singin.html')

def about(request):
    return render(request,'JobBazzar/about.html')

def profile(request):
    if request.session.get('userId') is not None:
        email = request.session.get('userId')
        value_exists = Profile.objects.filter(email=email).exists()
        if value_exists:
             data = Profile.objects.get(email=email)
             name1 = data.name
             age1 = data.age
             lan_list = data.language.split(",")
             skills_list = data.skills.split(",")
             achi_list = data.achievements.split(",")
            #  Check Experience Exist or Not
             if data.experience_field is not None:
                exp_c = 1
                fild_list = data.experience_field.split(",")
             else:
                  fild_list = []
                  exp_c = 0
                #   Check Project Details Exist Or Not
             if data.projects is not None:
                pro_c = 1
                proj_list = data.projects.split(",")
            
             else:
                  proj_list = []
                  pro_c = 0
            #  print(f"{lan_list} {skills_list} {proj_list}")
            #  print(data.profile_photo)
            #  print(age1)

             return render(request,'JobBazzar/profile.html',{"name":name1,"age":age1,"email":data.email,"location":data.location,"degree":data.degree,"phone":data.phone,"school":data.school,"collage":data.college,"experience":data.experience,"pYear":data.passingYear,"language":data.language,"linkedin":data.linkedin,"cgpa":data.cgpa,"skills":skills_list,"Projects":proj_list,"achievements":achi_list,"Photo":data.profile_photo,"Exp":fild_list,"Check_EXP":exp_c,"Check_PRO":pro_c})
        else:
             return redirect('UpdateProfile')
             
    else:
        return redirect('login')
    return render(request,"JobBazzar/profile.html")

def UpdateProfile(request):
    if request.session.get('userId') is not None:
        if request.method == 'POST':
            email = request.session.get('userId')
            name = request.POST.get("name")
            loc = request.POST.get('location')
            deg = request.POST.get('degree')
            phone =  request.POST.get('phone')
            school = request.POST.get('school')
            collage = request.POST.get('college')
            age = request.POST.get('age')
            experience = request.POST.get('experience')
            passYear = request.POST.get('passingYear')
            language = request.POST.get('language')
            linkedIn = request.POST.get('linkedin')
            cgpa = request.POST.get('cgpa')
            skils = request.POST.get('skills')
            work_exp = request.POST.get('workexp')
            # education = request.POST.get('')
            project = request.POST.get('projects')
            achivenment = request.POST.get('achievements')
            photo = request.FILES['profile_photo']
            ProfileAdd = Profile(email=email,name=name,location=loc,degree=deg,phone=phone,school=school,college=collage,age=age,experience=experience,passingYear=passYear,language=language,linkedin=linkedIn,cgpa=cgpa,skills=skils,projects=project,achievements=achivenment,profile_photo = photo,experience_field=work_exp,education="")
            ProfileAdd.save()
            return redirect('Profile')
        else:
             pass
        
    else:
        print("Session Not Found")
        return redirect('login')
    
    return render(request,"JobBazzar/AddProfile.html")

def editProfile(request):
    if request.session.get('userId') is not None:
        pdata = Profile.objects.get(email = request.session.get('userId'))
        if request.method == 'POST':
            email = request.session.get('userId')
            name = request.POST.get("name")
            loc = request.POST.get('location')
            deg = request.POST.get('degree')
            phone =  request.POST.get('phone')
            school = request.POST.get('school')
            collage = request.POST.get('college')
            age = request.POST.get('age')
            experience = request.POST.get('experience')
            passYear = request.POST.get('passingYear')
            language = request.POST.get('language')
            linkedIn = request.POST.get('linkedin')
            cgpa = request.POST.get('cgpa')
            skils = request.POST.get('skills')
            work_exp = request.POST.get('workexp')
            # education = request.POST.get('')
            project = request.POST.get('projects')
            achivenment = request.POST.get('achievements')
            # photo = request.FILES['profile_photo']
            Profile.objects.filter(email=request.session.get('userId')).update(email=email,name=name,location=loc,degree=deg,phone=phone,school=school,college=collage,age=age,experience=experience,passingYear=passYear,language=language,linkedin=linkedIn,cgpa=cgpa,skills=skils,projects=project,achievements=achivenment,experience_field=work_exp)

            return redirect('Profile')  
            # ProfileAdd.save()
        else:
             pass
        
    else:
        print("Session Not Found")
        return redirect('login')
    
    return render(request,"JobBazzar/AddProfile.html",{"profile":pdata})

def Forgot(request):
    secret_key = "#007DAP#acbs"
    if request.method == 'POST':
    
        ExistUser = username_exists(request.POST['email'])
        print(ExistUser)
        if(ExistUser == True):
                num = str(random.randint(100000, 999999))
                VAL = request.POST.get('email')
                html_content = '<html><body><p>Dear User,<br> <font style="color:#625AA8;font-size:18px;">'+num+'</font> is your one time password(OTP).<br>Please do not share the OTP with others.<br><br>Regards,<br><font style="color:#625AA8;font-size:15px;">Team Job Bazaar</font></p></body></html>'
                send_html_email(settings.EMAIL_HOST_USER,request.POST['email'],"Job Bazaar Reset Password OTP",html_content,settings.EMAIL_HOST,settings.EMAIL_PORT,"unlockhome07@gmail.com",settings.EMAIL_HOST_PASSWORD)
                value_to_encrypt = num
                encrypted_value= encrypt_value(value_to_encrypt, secret_key)
                MSG = encrypt_value(VAL, secret_key)
                request.session['OTP'] = encrypted_value;
                request.session['id'] = MSG
                request.session['email'] = VAL
                request.session['submit'] = "true";

                return redirect('Reset')
        else:
                messages.error(request,"User already not exist")
                return redirect('Forgot')
    return render(request,"JobBazzar/ForgotPassword.html")

def Reset(request):
    if request.session.get('submit') is not None and request.session.get('OTP') is not None:
        print("Sessoin  Found")
        if request.method == 'POST':
             print("POST FOUND")
             secret_key = "#007DAP#acbs"
             my_data = request.session.get('OTP', 'default_value')
             email = request.session.get('email')
             dec_email = email
             print(my_data)
             value = decrypt_value(my_data,secret_key)
             otp = request.POST['otp']
            #  print(otp)
             print("OTP : "+ otp)
             print("VALUE : "+ value)

             if otp == value :
                  print("Correct OTP")
                  if request.POST["password"] == request.POST["confirm"]:
                        print("Password Match")
                        # print(dec_email)
                        user = User.objects.get(username=dec_email)
                        user.set_password(request.POST['password'])
                        user.save()
                        del request.session['OTP']
                        del request.session['submit']
                #   request.session['auth'] = "done"
                #   print("Auth Created")
                        return redirect('login')
                  else:
                         messages.error(request,'password and confirm password does not match!')
             else:
                 messages.error(request,"Invalid OTP!")
    else:
        return redirect('Forgot')
                
    

    return render(request,"JobBazzar/ResetPassword.html")

def send_html_email(sender_email, recipient_email, subject, html_content, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach HTML content to the message
    message.attach(MIMEText(html_content, 'html'))

    # Connect to the SMTP server and send the message
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def encrypt_value(value, secret_key):
    signer = Signer(secret_key)
    encrypted_value = signer.sign(value)
    return encrypted_value

def decrypt_value(encrypted_value, secret_key):
    signer = Signer(secret_key)
    try:
        decrypted_value = signer.unsign(encrypted_value)
        return decrypted_value
    except Exception as e:
        # Handle decryption error (e.g., invalid signature)
        print(f"Error decrypting value: {e}")
        return None
    
def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    
    return False

def downloadCV(request,name,phone,location,email,ExpField,degree,collage,school,Pyear,cgpa,lin,Per,skills,language,achi,project,expYear):
     EXP = ExpField
     val2= []
    #  For Null Experience Remove
     if(EXP is not None):
          val1 = EXP.split(",")
          val2.append('<h2 class="h2">EXPERIENCE</h2>')
          val2.append('<div class="hr"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>')
          val2.append('<p class="icon" style="font-family:Sans-serif;font-size:20px; color:#0076FD;"><i class="fa fa-calendar" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;<b>EXPERIENCE : '+expYear+' YEARS </b></p>')
          for i in val1:
             val2.append( '<h3 class="h3 exp">'+i+'</h3></br>')
    #   html_content += '<p class="icon"><i class="fa fa-print" style="font-size:14px; color:#0076FD"></i>&nbsp;&nbsp;HSC : '+Per+'</p>'
     else:
          val2 = "<p></p>"
    

     #  For Null Project Remove
     val3= []
     if(EXP is not None):
          val4 = project.split(",")
          val3.append('<h2 class="h2">PROJECTS</h2>')
          val3.append('<div class="hr"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>')
          for i in val4:
             val3.append( '<h3 class="h3 exp">'+i+'</h3></br>')
    #   html_content += '<p class="icon"><i class="fa fa-print" style="font-size:14px; color:#0076FD"></i>&nbsp;&nbsp;HSC : '+Per+'</p>'
     else:
          val3 = "<p></p>"

     sk = skills.split(",")
     lan  = language.split(",")
     ach = achi.split(",")
        
     html_content = '<html>'
     html_content += '<head><title>Download CV</title>'
     html_content += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
     html_content += """<style>
   
     .h1{
        padding-top:30px;
        padding-left:50px;
        font-size:35px;
        margin-bottom:10px;
        font-family:Sans-serif;
     }
      *{ margin:0;}
     .h2{
        padding-top:15px;
        padding-left:50px;
        font-size:22px;
        font-family:Sans-serif;
        margin:5px;
     }
     .icon{
         padding-left:50px;
         font-family:Sans-serif;
         margin-bottom:2%;
     }
     .hr{
        height:10px;
        margin-bottom:2%;
        width:100%;
        padding-top:0px;
        margin-top:0px;
    
     }
     .h3{
        padding-left:50px;
        font-family:Sans-serif;
        margin-bottom:5px;
        
        
     }
     .exp{
     font-size:20px;
     }
     ul{
     padding-left:75px;
     font-family:Sans-serif;
     font-size:20px;
     list-style-type: square;
     padding-bottom:10px;
     }

     li{
        padding-top:5px;
        color:#0076FD;
        font-weight: 500;
     }
    
     </style></head>"""
     html_content += '<body>'

     html_content += '<h1 class="h1">'+name.upper()+'</h1>'
     html_content += '<p class="icon"><i class="fa fa-phone" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;'+phone+' &emsp; <i class="fa fa-envelope-open" aria-hidden="true" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;'+email+'&emsp;<i class="fa fa-linkedin" aria-hidden="true" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;'+lin+'</p>'
    #  html_content += '<p class="icon"><i class="fa fa-envelope-open" aria-hidden="true" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;'+email+'</p>'
     html_content += '<p class="icon"><i class="fa fa-map-marker" style="font-size:20px; color:#0076FD"></i>&nbsp;&nbsp;'+location+'</p>'
    
     html_content += '<h2 class="h2">EDUCATION</h2>'
     html_content += '<div class="hr"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>'
     html_content += '<h3 class="h3">'+degree.upper()+'</h3>'
     html_content += '<h3 class="h3"><font color="#0076FD" style="font-family:20px">'+collage+'</font></h3>'
     html_content += '<p class="icon"><i class="fa fa-calendar" style="font-size:14px; color:#0076FD"></i>&nbsp;&nbsp;'+Pyear+' &emsp;<i class="fa fa-print" style="font-size:14px; color:#0076FD"></i>&nbsp;&nbsp;CGPA : '+cgpa+'</p>'
     html_content += '<div class="hr" style="margin-bottom:1%;"><hr style="width:90%;margin-left:50px; border-top: 1px dotted gray;"></div>'
     html_content += '<h3 class="h3"><font style="font-family:20px">'+school.upper()+'</font></h3>'
     html_content += '<p class="icon"><i class="fa fa-print" style="font-size:14px; color:#0076FD"></i>&nbsp;&nbsp;HSC : '+Per+'</p>'

     html_content += '<h2 class="h2">SKILLS</h2>'
     html_content += '<div class="hr" style="margin-bottom:0%"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>'

     html_content += '<ul>'
     for s in sk:
          html_content += '<li>'+ s +'</li>'
     html_content += '</ul>'

     html_content += '<h2 class="h2">LANGUAGES</h2>'
     html_content += '<div class="hr" style="margin-bottom:0%"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>'
     html_content += '<ul>'
     for l in lan:
          html_content += '<li>'+ l +'</li>'
     html_content += '</ul>'

    
# For Project
     for data1 in val3:
          html_content += data1
    
# For Experiance

     for data in val2:
          html_content += data

     html_content += '<h2 class="h2">KEY ACHIEVEMENT | HOBBIES </h2>'
     html_content += '<div class="hr" style="margin-bottom:0%"><hr style="width:90%;margin-left:50px;background-color:black;height:3px;"></div>'
     html_content += '<ul>'
     for a in ach:
          html_content += '<li>'+ a +'</li>'
     html_content += '</ul>'






     html_content += '</body>'

     options = {
      'page-size': 'A4',
      'margin-top': '0mm',
      'margin-right': '0mm',
      'margin-bottom': '0mm',
      'margin-left': '0mm',
      }
     
     pdf = pdfkit.from_string(html_content,options=options)
   
    # Prepare the HTTP response with the PDF content
     response = HttpResponse(pdf, content_type='application/pdf')
     response['Content-Disposition'] = 'attachment; filename="'+name+' Resume.pdf"'

     return response

def dowload_call(request):
     if request.session.get('userId') is not None:
        email =request.session.get('userId')
        value_exists = Profile.objects.filter(email=email).exists()
        if value_exists:
               data = Profile.objects.get(email=email)
               name = data.name
               phone = data.phone
               persentage = "77%"
               return downloadCV(request,name,phone,data.location,data.email,data.experience_field,data.degree,data.college,data.school,data.passingYear,data.cgpa,data.linkedin,persentage,data.skills,data.language,data.achievements,data.projects,data.experience)

        else:
             return redirect('Home')
     else:
          return HttpResponse('404 Page Not Found')
     
# Admin 
def CompanyLogin(request):
    add = "Company"
    secret_key = "#007DAP#acbs"
    if request.method == 'POST':
    
        ExistUser = company_exists(request.POST['email'])
        print(ExistUser)
        if(ExistUser == False):
                num = str(random.randint(100000, 999999))
                VAL = request.POST.get('email')
                html_content = '<html><body><p>Dear User,<br> <font style="color:#625AA8;font-size:18px;">'+num+'</font> is your one time password(OTP).<br>Please do not share the OTP with others.<br><br>Regards,<br><font style="color:#625AA8;font-size:15px;">Team Job Bazaar</font></p></body></html>'
                send_html_email(settings.EMAIL_HOST_USER,request.POST['email'],"Job Bazaar OTP",html_content,settings.EMAIL_HOST,settings.EMAIL_PORT,"unlockhome07@gmail.com",settings.EMAIL_HOST_PASSWORD)
                value_to_encrypt = num
                encrypted_value= encrypt_value(value_to_encrypt, secret_key)
                MSG = encrypt_value(VAL, secret_key)
                request.session['OTP'] = encrypted_value;
                request.session['id'] = MSG
                request.session['email'] = VAL
                request.session['submit'] = "true";

                return redirect('CVerify')
        else:
                messages.error(request,"Company already exist")
                return redirect('CRegister')
     
    return render(request,'JobBazzar/Register.html',{"com":add})
             
          
def company_exists(username):
    if Company.objects.filter(email=username).exists():
        return True
    
    return False


def Cverify(request):
    print("Verify Calling")
    if request.session.get('submit') is not None and request.session.get('OTP') is not None:
        print("Sessoin  Found")
        if request.method == 'POST':
             print("POST FOUND")
             secret_key = "#007DAP#acbs"
             my_data = request.session.get('OTP', 'default_value')
             print(my_data)
             value = decrypt_value(my_data,secret_key)
             one = request.POST['one']
             two = request.POST['two']
             thr = request.POST['thr']
             fore = request.POST['fou']
             fiv = request.POST['fiv']
             six = request.POST['six']
             otp = one+two+thr+fore+fiv+six
            #  print(otp)
             print("OTP : "+ otp)
             print("VALUE : "+ value)

             if otp == value :
                  del request.session['OTP']
                  del request.session['submit']
                  request.session['auth'] = "done"
                  print("Auth Created")
                  return redirect('CompanyD')
             else:
                 messages.error(request,"Invalid OTP")
    else:
        return redirect('AdminLogin')
    return render(request,'JobBazzar/verify.html')

def Register_Company(request):
    secret_key = "#007DAP#acbs"
    if request.session.get( 'auth' ) == 'done':
        if(request.method=='POST'):
            dec_email = decrypt_value(request.session.get('id'),secret_key)
            print(dec_email)
            passwords = encrypt_value(request.POST.get('password'),secret_key) 
            Add_Com = Company(email=dec_email,company_name=request.POST.get('companyName'),founded=request.POST.get('foundedIn'),phone=request.POST.get('phone'),location=request.POST.get('location'),primary_industry=request.POST.get('location'),website=request.POST.get('website'),password=passwords,logo=request.FILES['logo'])
            Add_Com.save()
            # return HttpResponse("Success")
            return redirect('dlogin')

            #  print(dec_email)
             
    else:
         return redirect('CompanyLogin')
    return render(request,'JobBazzar/CompanyRegisterForm.html')

def CLogin(request):
     secret_key = "#007DAP#acbs"
     if Company.objects.filter(email=request.POST.get('email')).exists():
        if request.method == "POST":
             login = Company.objects.get(email=request.POST.get('email'))
             if  login.password == encrypt_value(request.POST.get('Password'),secret_key):
                  request.session['admin'] = "true"
                  request.session['adminUID'] = request.POST.get('email')

                  return redirect('dashbord')
             else:
                    messages.error(request,"Invalid Email  or Password")
                    return render(request,'JobBazzar/singin.html')
                  
    
     return render(request,'JobBazzar/singin.html')

def dashbord(request):
     if request.session.get('admin') == 'true':
        uid = request.session.get('adminUID')
        # print(uid)
        company = Company.objects.get(email=uid)
        c_name = company.company_name
        listed_jobs = Job.objects.filter(emails=uid)
        request.session['action'] = "yes"
        count = Job.objects.filter(emails=uid).count()
        count_Application = Application.objects.filter(company_email=uid).count()
        count_Pending = Application.objects.filter(**{"company_email":uid,"status":"Pending"}).count()
        count_interview = Application.objects.filter(**{"company_email":uid,"status":"Accepted"}).count()




        # print(f"name : {c_name}")
        if request.method == "POST":
             ids = random.randint(10000, 99999)
             j_id = "JB"+str(ids)
            #  print(j_id)
             AddJob(uid,request.POST.get('title'),c_name,request.POST.get('location'),request.POST.get('hour'),request.POST.get('category'),request.POST.get('rate'),request.POST.get('salary'),request.POST.get('desc'),request.POST.get('res'),request.POST.get('skills'),request.POST.get('exp'),request.POST.get('time'),'Private','Urgent',j_id,request.FILES['logo'],request.POST.get('skil1'), request.POST.get('skil2'),request.POST.get('skil3'),request.POST.get('zip'))
        return render(request,'JobBazzar/dashbord.html',{"company_name":c_name,"listed_jobs":listed_jobs,"count":count,"CA":count_Application,"CP":count_Pending,"CI":count_interview})
     else:
          return redirect('dlogin')

def AddJob(email,jt,cn,loc,hr,cat,rate,sal,jd,kr,skills,exp,time,jty,need,id,logos,skil1,skil2,skil3,zip):
    # if request.session.get('auth') == 'true':
    #         if request.method == "POST":
               addJob = Job(emails=email,job_title=jt,company_name=cn,location=loc,hours=hr,category=cat,rate=rate,salary=sal,job_description=jd,key_responsibilities=kr,skill=skills,experience=exp,time=time,job_type=jty,need=need,id=id,logo=logos,skill1=skil1,skill2=skil2,skill3=skil3,zipcode=zip)
               addJob.save()

def delete(request,id):
    #  val = request.GET.get('id','not find')
     if request.session.get('action') == "yes":
        delete = Job.objects.filter(id=id).delete()
        return redirect('dashbord')
     else:
          return redirect('dashbord')
     
def application_view(request,id,sc):
     if(request.session.get('action') == "yes"):
         if(request.session.get('adminUID') == sc):
            try:
                listed_Vec = Application.objects.filter(**{"job_id":id,"status":"Pending"})
                listed_Vec_done = Application.objects.filter(**{"job_id":id,"status":"Accepted"})                
                name = listed_Vec[0].job_title
                return render(request,'JobBazzar/Vacency_application_list.html',{"lv":listed_Vec,"Job":name,"selected":listed_Vec_done})
            
            except:
                 return HttpResponse("<script> alert('No One Applied For this Job'); window.location.replace('/dashbord'); </script>")
     else:
        redirect('dashbord')

def job(request):
    if request.session.get('login') == "true":
        # name="Login/Reg"
        if(request.session['userId'] != None):
             em = request.session.get('userId')
             data = Profile.objects.get(email=em)
             name = data.name
        Jobs = Job.objects.all()
        li=""
        jc=""
        count = len(Jobs)
        titles = Job.objects.all()
        for i in range(0,count):
            li += titles[i].job_title+"," 
            jc += titles[i].category+","
        if request.method == "POST":
            if (len(request.POST.get('title', '')) != 0) and (len(request.POST.get('zip', '')) == 0) and (request.POST.get('category', None) is None):  
                   val =request.POST.get('title')
                   request.session['field'] = 1
                   return redirect('job_filter', id=val)  

            elif (len(request.POST.get('title', '')) == 0) and (len(request.POST.get('zip', '')) != 0) and (request.POST.get('category', None) is None):  
                   request.session['field'] = 2
                   z = request.POST.get('zip')
                   return redirect('job_filter', id=z)  
            
            elif (len(request.POST.get('title', '')) == 0) and (len(request.POST.get('zip', '')) == 0) and (request.POST.get('category', None) is not None):  
                    request.session['field'] = 3
                    return redirect('job_filter', id=request.POST.get('category'))  
            
            elif (len(request.POST.get('title', '')) != 0) and (len(request.POST.get('zip', '')) != 0) and (request.POST.get('category', None) is None):  
                request.session['field'] = 1
                request.session['field1'] = 2
                return redirect('job_filter2', zip=request.POST.get('zip'),tit=request.POST.get('title'))  

            elif (len(request.POST.get('title', '')) != 0) and (len(request.POST.get('zip', '')) == 0) and (request.POST.get('category', None) is not None):  
                print("title+category")
                request.session['field'] = 1
                request.session['field1'] = 3
                return redirect('job_filter2', zip=request.POST.get('zip'),tit=request.POST.get('category'))

            elif (len(request.POST.get('title', '')) == 0) and (len(request.POST.get('zip', '')) != 0) and (request.POST.get('category', None) is not None):  
                print("category + map")
                request.session['field'] = 2
                request.session['field1'] = 3
                return redirect('job_filter2', zip=request.POST.get('zip'),tit=request.POST.get('category'))
            
            elif (len(request.POST.get('title', '')) != 0) and (len(request.POST.get('zip', '')) != 0) and (request.POST.get('category', None) is not None):
                request.session['field'] = 2
                return redirect('job_filter3', tit=request.POST.get('zip'),zip=request.POST.get('zip'),cat=request.POST.get('category'))
                 
        return render(request,'JobBazzar/ShowJob.html',{"allJob":Jobs,"jt":li,"jc":jc,"name":name})
    else:
         return redirect('login')
     
def job_filter(request,id):
    # print(id[0])
    if request.session.get('field') is not None:

        val = request.session.get('field')
        field = getField(val)
    # Jobs = Job.objects.filter(job_title=id)
        Jobs = Job.objects.filter(**{field: id})
        li=""
        jc = ""
        count = len(Jobs)
        titles = Job.objects.all()
        for i in range(0,count):
            li += titles[i].job_title+"," 
            jc += titles[i].category+","
        del request.session['field']
        # del request.session['field1']

        return render(request,'JobBazzar/ShowJob.html',{"allJob":Jobs,"jt":li,"jc":jc})
    else:
         return redirect('job')

def job_filter2(request,tit,zip):
    # print(id[0])
    if request.session.get('field') is not None:
        val = request.session.get('field')
        val1 = request.session.get('field1')

        field1,field2 = getTwoField(val,val1)
    # Jobs = Job.objects.filter(job_title=id)
        Jobs = Job.objects.filter(**{field1:tit,field2:zip})
        li=""
        jc = ""
        count = len(Jobs)
        titles = Job.objects.all()
        for i in range(0,count):
            li += titles[i].job_title+"," 
            jc += titles[i].category+","
        del request.session['field']
        del request.session['field1']

        return render(request,'JobBazzar/ShowJob.html',{"allJob":Jobs,"jt":li,"jc":jc})
    else:
         return redirect('job')
    
def job_filter3(request,tit,zip,cat):
    # print(id[0])
    if request.session.get('field') is not None:
        val = request.session.get('field')
        val1 = request.session.get('field1')
        field1 = "job_title"
        field2 = "zipcode"
        field3 = "category"

        field1,field2 = getTwoField(val,val1)
    # Jobs = Job.objects.filter(job_title=id)
        Jobs = Job.objects.filter(**{field1:tit,field2:zip,field3:cat})
        li=""
        jc = ""
        count = len(Jobs)
        titles = Job.objects.all()
        for i in range(0,count):
            li += titles[i].job_title+"," 
            jc += titles[i].category+","
        del request.session['field']  
        return render(request,'JobBazzar/ShowJob.html',{"allJob":Jobs,"jt":li,"jc":jc})
    else:
         return redirect('job')


def getField(val):
     if(val == 1):
        return "job_title"
     elif(val == 2):
        return "zipcode"
     else:
          return "category"
     
def getTwoField(val1,val2):
     if(val1 == 1) and (val2 == 2):
          return "job_title","zipcode"
     elif(val1 == 1) and (val2 == 3):
          return "job_title","category"
     else:
        #   (val1 == 2) and (val2 == 3):
          return "zipcode","category"
     
def jobupdate(request,id,email):
    if request.session.get('action') == "yes":
         if(request.session.get('adminUID') == email):
            jdata = Job.objects.get(id = id)
            if request.method == "POST":
                Job.objects.filter(id=id).update(job_title=request.POST.get('title'),location=request.POST.get('location'),hours=request.POST.get('hour'),rate=request.POST.get('rate'),salary=request.POST.get('salary'),job_description=request.POST.get('desc'),key_responsibilities=request.POST.get('res'),skill=request.POST.get('skills'),experience=request.POST.get('exp'),skill1=request.POST.get('skil1'),skill2=request.POST.get('skil2'),skill3=request.POST.get('skil3'),zipcode=request.POST.get('zip'))     
                return redirect('dashbord')
            #   return HttpResponse("yes")
            return render(request,'JobBazzar/update.html',{"jdata":jdata})
    return HttpResponse("Not Valid User")          

def job_details(request,id):
     if request.session.get('login') == "true":
          if(Job_exists(id)):
               name="Login"
               if(request.session['userId'] != None):
                    em = request.session.get('userId')
                    data = Profile.objects.get(email=em)
                    name = data.name
               j_data = Job.objects.get(id=id)
               cemail = j_data.emails
               c_data = Company.objects.get(email=cemail)
               key_res = j_data.key_responsibilities.split(",")
               skills = j_data.skill.split(",")
               sugg = Job.objects.filter(category=j_data.category)[:4]
               if request.method == "POST":
                    if len(request.POST.get('Name')) != 0 and  bool(request.FILES.get('cv', False)) == True:
                        if Application_exists(id,j_data.job_title,request.session.get('userId')) == False:
                        # print(f"User Exist : {Application_exists(id,j_data.job_title,request.session.get('userId'))}")
                            ids = random.randint(10000, 99999)
                            a_id = "JBAP"+str(ids)
                            name = request.POST.get('Name')
                            file = request.FILES.get('cv')
                            email = request.session.get('userId')
                            j_id = id
                            jt = j_data.job_title
                            company = c_data.company_name
                            App = Application(name=name,applicant_email=email,company_email=cemail,job_id=j_id,job_title=jt,cv=file,id=a_id,company=company)
                            App.save()
                            return redirect('SA')
                        else:
                             return HttpResponse("<script> alert('you have already applied for this JOB'); window.location.replace('/Job'); </script>")
                    else:
                         return HttpResponse("<script>alert('Not Valid Request');</script>")
               return render(request,"JobBazzar/Job_details.html",{"jdata":j_data,"cdata":c_data,"keyRes":key_res,"skill":skills,"sugg":sugg,"name":name,"name":name})
          else:
               previous_page = request.META.get('HTTP_REFERER')
               if previous_page:
            #    print(previous_page)
                    return redirect(previous_page)
               else:
                     return redirect("Home")
     else:
          return redirect('login')
     

def Job_exists(val):
    if Job.objects.filter(id=val).exists():
        return True
    
    return False

def Application_exists(val,tit,email):
    if Application.objects.filter(**{"job_id":val,"job_title":tit,"applicant_email":email}).exists():
        return True
    
    return False
def Action(request,id,val,email):
      if(request.session.get('action') == "yes"):
         if(request.session.get('adminUID') == email):
            #  return HttpResponse(f"{id}-{val}-{email}")
            if(val == "X0xvVq+DvGV0f+b98xEnyQ=="):
                 try:
                    up =  Application.objects.filter(id=id).update(status="Rejected")
                    return HttpResponse("<script> history.back();</script>")
                 except:
                    return HttpResponse("<script>alert('Not Valid Request'); history.back();</script>")
                 
            elif(val == "xiK8as2h6OCmpTU47kyYTg=="):
                if(request.method == "POST"):
                    date = request.POST.get('date')
                    time = request.POST.get('time')
                    accepted = "Accepted"
                    interview = date+" - "+time
                    up =  Application.objects.filter(id=id).update(status=accepted,interview=interview)
                    em = Application.objects.get(id=id)
                    # print(em.company_email)
                    # print(em.company_email)
                    jb = Company.objects.get(email=em.company_email)
                    name = em.name
                    e_mail = em.applicant_email

                    data = """
                    

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application Confirmation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #4CAF50;
            text-align: center;
        }
        p {
            margin-bottom: 15px;
        }
        ul {
            margin-bottom: 15px;
            padding-left: 20px;
        }
        ul li {
            list-style: none;
            margin-bottom: 5px;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            color: #888888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Congratulations!</h2>
        <p>Dear """+name+""",</p>
        
        <p>We are delighted to inform you that you have been selected for an interview at <strong style="color: #4CAF50;">"""+em.company+"""</strong> for the position of <strong>"""+em.job_title+"""</strong>.</p>

        <p><strong>Interview Details:</strong></p>
        <ul>
            <li><strong>Date:</strong> """+request.POST.get('date')+"""</li>
            <li><strong>Time:</strong> """+request.POST.get('time') +"""</li>
            <li><strong>Location:</strong> """+jb.location+"""</li>
        </ul>

        <p style="color: #4CAF50;">We look forward to meeting with you and discussing your qualifications further.</p>

        <p>Best regards,</p>
        <p>JobBazaar<br>
       

        <p class="footer"><em>*Please note that this is an automated email. Do not reply to this email address.</em></p>
    </div>
</body>
</html>
"""
                    send_html_email(settings.EMAIL_HOST_USER,e_mail,"Congratulations Your Application has been Selected!",data,settings.EMAIL_HOST,settings.EMAIL_PORT,"unlockhome07@gmail.com",settings.EMAIL_HOST_PASSWORD)
                    return redirect("dashbord")
                return render(request,"JobBazzar/interview.html")

            else:
                 return HttpResponse("<script>alert('Not Valid Request'); history.back();</script>")
            
         else:
                return HttpResponse("<script>alert('Not Valid Request'); window.location.replace('/dashbord');</script>")
      else:
           return redirect('dashbord')
      
def showCat(request,cat):
      if request.session.get('login') == "true":
        Jobs = Job.objects.filter(category=cat)
        return render(request,"JobBazzar/jobCat.html",{"catjob":Jobs})
      
def ShowApplication(request):
      if request.session.get('userId') is not None:
           up =  Application.objects.filter(applicant_email=request.session.get('userId'))
           return render(request,"JobBazzar/Applications.html",{"data":up})
     

     
     

          
          
          
     
     
     