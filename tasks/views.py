from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile, extendeduser
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def tasks(request):
    profile = Profile.objects.get(user = request.user)
    rec_count = len(request.user.rec_to.all())
    try:
        donor = extendeduser.objects.get(user=request.user)
        donated = 1
    except:
        donated = 0
    context = {'ref_code': profile.code, 'rec_count': rec_count, 'donated':donated, 'title':"LeukeAware | Earn Badges!"}

    return render(request, 'tasks/tasks.html', context)

def popup(request):
    return render(request,"tasks/popup.html")