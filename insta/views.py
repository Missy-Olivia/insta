from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt


# Create your views here.
def signup(request):
    if request.user.is_authenticated():
        return redirect('insta')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                new_profile = Profile(user=user)
        else:
            form = SignupForm()
    return render(request, 'registration/registration.html',{'form':form})
