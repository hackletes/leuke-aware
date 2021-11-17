from django.urls import path
from . import views





urlpatterns = [
    
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    # path('logout/',views.logoutUser,name='logout'),
    path('SignUp/',views.signup,name='register'),
    path('login-signup/',views.LS,name='LS'),
    # path('profile/',views.profile,name='profile'),
]
