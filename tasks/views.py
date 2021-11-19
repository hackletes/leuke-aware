from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile, extendeduser

# Create your views here.

def tasks(request):
    profile = Profile.objects.get(user = request.user)
    rec_count = len(request.user.rec_to.all())
    try:
        donor = extendeduser.objects.get(user=request.user)
        donated = 1
    except:
        donated = 0
    context = {'ref_code': profile.code, 'rec_count': rec_count, 'donated':donated}

    return render(request, 'tasks/tasks.html', context)