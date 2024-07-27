from django.urls import path
from . import views
from django.contrib import admin
# for file upload
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",views.Home,name="Home"),
    path("signin",views.signin,name="signin"),
    path("Register",views.register,name="Register"),
    path("Verify",views.verify,name="Verify"),
    path("login",views.logins,name="login"),
    path("About",views.about,name="About"),
    path("Profile",views.profile,name="Profile"),
    path("UpdateProfile",views.UpdateProfile,name="UpdateProfile"),
    path("editProfile",views.editProfile,name="editProfile"),
    path("ForgotPassword",views.Forgot,name="Forgot"),
    path("ResetPassword",views.Reset,name="Reset"),
    path("Download",views.dowload_call,name="downloadCall"),
    path("createadmin",views.CompanyLogin,name="AdminLogin"),
    path("CompanyRegister",views.CompanyLogin,name="CRegister"),
    path("CompanyVerify",views.Cverify,name="CVerify"),
    path("CompanyDetails",views.Register_Company,name="CompanyD"),
    path("dashbordlogin",views.CLogin,name="dlogin"),
    path("jobupdate/<id>/<email>",views.jobupdate,name="jupdate"), 
    path("dashbord",views.dashbord,name="dashbord"),
    path('delete/<id>', views.delete, name='delete'),
    path('dashbord/<id>/<sc>', views.application_view, name='av'),
    path('Job', views.job, name='job'),
    path('Job/<id>', views.job_filter, name='job_filter'),
    path('Job/<tit>/<zip>', views.job_filter2, name='job_filter2'),
    path('Job/<tit>/<zip>/<cat>', views.job_filter3, name='job_filter3'),
    path('Jobs/<id>', views.job_details, name='showJob'),
    path('Action/<id>/<val>/<email>', views.Action, name='Action'),
    path('job/<cat>',views.showCat,name='jobcat'),
    path('Applications',views.ShowApplication,name='SA'),





    # path('Job/<zip>', views.job_filter1, name='job_filter1'),




















]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)