from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.http.response import HttpResponse, HttpResponseRedirect
from django.db.models import Q

import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.


def referral(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session["ref_profile"] = profile.pk
        print("session",request.session["ref_profile"])
        return redirect("LS")
    except:
        return redirect("home")

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


                    if (len(request.POST['password1']) <8):
                        messages.error(request, "Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value")
                        return render(request, 'users/LS.html')

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
                        #Creating User
                        user = User.objects.create_user( username =request.POST['email'], password=request.POST['password1'],email=request.POST['email'],first_name=request.POST['firstname'])
                        
                        messages.success(request, f'Your account has been Create!! Login Now')

                        #Refering user
                        profile_id = request.session.get("ref_profile")
                        print("id:", profile_id)
                        if profile_id is not None:
                            recommending_user = Profile.objects.get(pk = profile_id).user
                            current_user_profile = Profile.objects.get(user=user)
                            current_user_profile.recommended_by = recommending_user
                            current_user_profile.save()
                        auth.login(request, user)

                        return redirect(LS)
            else:
                return render(request, 'users/LS.html', {'msg': ["Passwords Don't match"]})
        else:
            return render(request, "users/LS.html")

def LS(request):
    print(request.session.get("ref_profile"))
    return render(request, "users/LS.html")

def about(request):
    pass

def tasks(request):
    pass

def profile(request):
    pass

def logout(request):
    auth.logout(request)
    return redirect("home")

def chatbot(request):
    return render(request, 'users/chatbot.html')


@login_required(login_url='login')
def DR(request):
            return render(request,'users/DR.html')

def Donars(request):
        if request.method == 'POST':
        
            number = request.POST['number']
            gender=request.POST['gender']
            age=request.POST['age']
            bldgrp=request.POST['bldgrp']
            address=request.POST['address']

            newextendeduser = extendeduser( number=number, gender=gender, age=age ,bldgrp=bldgrp, address= address, user=request.user)
            newextendeduser.save()
            messages.success(
                        request, f'Your data is saved')
            return render(request, "users/DR.html")
        else:
            return render(request,'users/DR.html')

def reciver(request):
        if request.method == 'POST':
        
            number = request.POST['number']
            gender=request.POST['gender']
            age=request.POST['age']
            bldgrp=request.POST['bldgrp']
            address=request.POST['address']

            newReciver = Reciver(  user=request.user ,number=number, gender=gender, age=age ,bldgrp=bldgrp, address= address)
            newReciver.save()
            messages.success(
                        request, f'Your data is saved')
            return render(request, "users/DR.html")
        else:
            return render(request,'users/DR.html')

def dkms(request):
    return render(request, "users/dkms.html")

@login_required(login_url='login')
def profile(request):
    datas = extendeduser.objects.filter(user = request.user)
    return render(request,'users/profile.html',{'data':datas})

@login_required(login_url='login')
def editprofile(request):
    context = {}
    
    edit = extendeduser.objects.get(user=request.user)
    context["edit"]=edit



    if request.method=="POST":
        number = request.POST['number']
        gender=request.POST['gender']
        age=request.POST['age']
        bldgrp=request.POST['bldgrp']
        address=request.POST['address']



        edit.number = number
        edit.gender = gender
        edit.age = age
        edit.bldgrp = bldgrp
        edit.address = address
        edit.save()



        context["status"] = "Changes Saved Successfully"
        return redirect(profile)
    return render(request,'users/editprofile.html' ,context)




def blog(request):
    return render(request, "users/Blog.html")


def about(request):
    return render(request, "users/About.html")    