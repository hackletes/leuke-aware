from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.db.models import Q

import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.


def home(request):
    return render(request, 'users/home.html')

def login(request):
    if request.method == 'POST':
        
        user = auth.authenticate( username =request.POST['email'], password=request.POST['password1'])
        if user is not None:
            auth.login(request,user)
            return render(request,'users/result.html')
            # return render(request,'users/result.html')
        
        else:
            messages.error(request, "invalid login credentials")
            return redirect("LS")
    else:
        return render(request,'users/LS.html')




def signup(request):
        if request.method == "POST":
            print("register called")

            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    messages.error(request,'email already exist')
                    # return render(request, 'users/LS.html', {'error': "username already exist"})

                except User.DoesNotExist:
                    # user = User.objects.create_user(username=request.POST['username'],password= request.POST['password1'],email= request.POST['email'])
                    # user = User.objects.create_user(username=request.POST['username'],password= request.POST['password1'])


                    if (len(request.POST['password1']) < 10):
                        return render(request, 'users/LS.html', {'error': "Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value"})

                    elif not re.search(r"[\d]+", request.POST['password1']):
                        return render(request, 'users/LS.html', {'error': "Your Password must contain Atleast 1 Numeric value "})
                    elif not re.findall('[A-Z]', request.POST['password1']):
                        return render(request, 'users/LS.html', {'error': "Your Password must contain Atleast 1 UpperCase Letter "})

                    elif not re.findall('[a-z]', request.POST['password1']):
                        return render(request, 'users/LS.html', {'error': "Your Password must contain Atleast 1 lowercase Letter "})
                    elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', request.POST['password1']):
                        return render(request, 'users/LS.html', {'error': "Your Password must contain Atleast 1 Specail character "})
                    elif not re.findall('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', request.POST['email']):
                        return render(request, 'users/LS.html', {'error': "Email ID is not Valid"})

                    else:
                            
                            user = User.objects.create_user( username =request.POST['email'], password=request.POST['password1'],email=request.POST['email'],first_name=request.POST['firstname'])
                            auth.login(request, user)
                            messages.success(
                                request, f'Your account has been Create!! Login Now')

                            return redirect(LS)
            else:
                return render(request, 'users/LS.html', {'msg': ["Passwords Don't match"]})
        else:
            return render(request, "users/LS.html")

def LS(request):
    return render(request, "users/LS.html")

