from django.shortcuts import render,redirect
from .forms import FormSignUp
from django.contrib.auth import login
# Create your views here.
def SignUp(request):
    if request.user.is_authenticated:
        return redirect('Aff')
    form=FormSignUp()
    if request.method=="POST":
        form=FormSignUp(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('Aff')
    return render(request,'Person/SignUp.html',
                  {'f':form})
