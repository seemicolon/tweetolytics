from django.shortcuts import render, redirect
from django.http import HttpResponse
from .import twitterAPI
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from dashboard.models import Project
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import Register
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordChangeForm

# Create your views here.
def register(request):

    form=Register()
    if request.method=="POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form=Register()


    return render(request, 'register.html',{'form':form})


def loginUser(request):


    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user=authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                p = Project.objects.filter(user_id=request.user.id)
                if p.count()>0:
                    return redirect('home')
                else:
                    return redirect('createProject')
            else:
                messages.error(request,'Username or Password is Incorrect!')
        else:
            messages.error(request,'Fill out all the fields')
    return render(request,'login.html')



def logoutUser(request):
    # del request.session["Is_Logged_In"]
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def createProject(request):
    if request.method=="POST":
        name=request.POST['cpfield']
        ins=Project(user_id=request.user.id,name=name)
        ins.save()
        return redirect('search')
    return render(request,'create_project.html')


@login_required(login_url='login')
def search(request):
    trend=twitterAPI.twitterTrends()
    return render(request,'search.html',{'trend':trend})


@login_required(login_url='login')
def dashboard(request):
    n = request.user.username
    return render(request,'dbase.html',{'name':n})


@login_required(login_url='login')
def projects(request):
    p=Project.objects.filter(user_id=request.user.id)
    return render(request,'projects.html',{'projects':p})


@login_required(login_url='login')
def profile(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            u=form.save()
            update_session_auth_hash(request, u)
            messages.success(request,"Password is Changed")
            return redirect('profile')
        else:
            messages.error(request, "Password is not Changed")

    else:
        form=PasswordChangeForm(request.user)
    info=request.user
    context={'info':info,'form':form}
    return render(request,'profile.html',context)


@login_required(login_url='login')
def home(request):
    labels=['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    data=[12, 19, 3, 5, 2, 3]
    n = request.user.username
    return render(request,'dashboard.html',{'labels':labels,'data':data,'name':n})


