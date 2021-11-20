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
from django.core.mail import send_mail

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
    return render(request, 'users/home.html', {'title': 'LeukeAware | Home'})

def login(request):
    if request.method == 'POST':
        user = auth.authenticate( username =request.POST['email'], password=request.POST['password1'])
        if user is not None:
            auth.login(request,user)
            prof = Profile.objects.get(user= user)
            if prof.is_blood_bank:
                return(redirect("blood-bank"))
            return redirect("home")
            # return render(request,'users/result.html')
        
        else:
            messages.error(request, "invalid login credentials")
            return redirect("LS")
    else:
        return redirect("LS")




def signup(request):
        if request.method == "POST":
            print("register called")

            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    messages.error(request,'email already exist')
                    return redirect('LS')
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
                        send_mail(
                                    ['Hello {} — thank you for signing up!'.format(user.first_name)],
                                    'Signup Succesfull, We are glad that you joined us.Explore the site and if possiible please register as a donor or any urgent requirement of blood please fill the reciver form we will help you out at our best.Thank you.',
                                    'leukeaware@gmail.com',
                                    ['{}'.format(user.email)],
                                    fail_silently=False,
                                )

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
            send_mail(
                        'Thanks for connecting with us!',
                        'Thank you for donating blood. You have played a very important role in our mission to save lives. Is it going too far to say you are a hero? We don’t think it is! So wear your invisible cape with pride, and start perfecting your catchphrase.We appreciate your efforts. The world needs more heroes like you! ',
                        'leukeaware@gmail.com',
                        ['{}'.format(request.user.email)],
                        fail_silently=False,
                )
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
            maildraft = f'we need bloodgroup {bldgrp } on urgent basis for{request.user.first_name} {gender} with age {age} email id {request.user.email } and address {address}'
            send_mail(
                        'thanku',
                        maildraft,
                        'leukeaware@gmail.com',
                        ['neerajbuakne@gmail.com' , 'sarveshvarade873@gmail.com' , 'nikitakarande27@gmail.com' ,'devrajshetake@gmail.com'],
                        fail_silently=False,
                )
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
    
    try:
        edit = extendeduser.objects.get(user=request.user)
    except:
        edit = None
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

def blood_bank(request):
    profiles = extendeduser.objects.all()
    context = {'profiles':profiles} 
    return render(request, 'users/bloodbank.html', context)


#################################################################################
from django.views.generic.base import TemplateView

class ExcelPageView(TemplateView):
    template_name = "result.html"

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [ 'First Name', 'Gender','Age', 'bloodgroup' ,'Email Address', 'phone number' 'Address' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = extendeduser.objects.all().values_list('user', 'gender', 'age' ,'bldgrp','id', 'number','address'  )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response