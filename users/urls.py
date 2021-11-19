from django.urls import path
from . import views





urlpatterns = [
    
    path('',views.home,name='home'),
    path('referral/<str:ref_code>/',views.referral,name='referral'),
    path('login/',views.login,name='login'),
    path('about/',views.about,name='about'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('SignUp/',views.signup,name='register'),
    path('login-signup/',views.LS,name='LS'),
    path('chatbot/',views.chatbot,name='chatbot'),
    path('donor/',views.Donars,name='Donars'),
    path('reciver/',views.reciver,name='reciver'),
    path('blood-donation/',views.DR,name='DR'),
    path('dkms/',views.dkms,name='dkms'),
    path('blog/',views.blog,name='blog'),
    path('about/',views.blog,name='about'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('blood-bank',views.blood_bank,name='blood-bank'),
    path('excel', views.ExcelPageView.as_view(), name='excel'),
    path('export/excel', views.export_users_xls, name='export_excel'),

] 
