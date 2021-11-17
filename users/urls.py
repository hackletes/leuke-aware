from django.urls import path
from . import views





urlpatterns = [
    
    path('',views.home,name='home'),
    path('referral/<str:ref_code>/',views.referral,name='referral'),
    path('login/',views.login,name='login'),
    path('about/',views.about,name='about'),
    path('logout/',views.logout,name='logout'),
    path('earn-badges/',views.tasks,name='tasks'),
    path('profile/',views.profile,name='profile'),
    # path('logout/',views.logoutUser,name='logout'),
    path('SignUp/',views.signup,name='register'),
    path('login-signup/',views.LS,name='LS'),
    # path('profile/',views.profile,name='profile'),
]
