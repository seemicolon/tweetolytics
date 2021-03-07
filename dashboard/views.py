# Import the libraries
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from django.shortcuts import render, redirect
from .import twitterAPI
from django.contrib.auth import login,authenticate,logout
from dashboard.models import Project
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from .forms import Register
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordChangeForm
from .twitterAPI import main

# Create your views here.
def register(request):

    form=Register()
    if request.method=="POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User registered successfully")
            return redirect('login')

    else:
        form=Register()
    return render(request, 'register.html',{'form':form})

@user_passes_test(lambda user: not user.username, login_url='projects', redirect_field_name=None)
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
                    return redirect('projects')
                else:
                    return redirect('search')
            else:
                messages.error(request,'Username or Password is Incorrect!')
        # else:
        #     messages.error(request,'Fill out all fields')
    return render(request,'login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
# def createProject(request):
#     if request.method=="POST":
#         name=request.POST['cpfield']
#         p=Project(user_id=request.user.id,name=name)
#         p.save()
#         global pId
#         pId=p.pk
#         print("kkk",pId)
#         return redirect('search')
#     return render(request,'create_project.html')

@login_required(login_url='login')
def search(request):
    if request.method == "POST":
        keyword= request.POST.get('search_field', False)
        tweett = main(keyword)
        total = tweett[0]
        pos = tweett[1]
        neg = tweett[2]
        neu = tweett[3]
        ang = tweett[4]
        hap = tweett[5]
        wc = tweett[6]
        p = Project(user_id=request.user.id, name=keyword,total=total,positive=pos,
                    negative=neg,neutral=neu,angry=ang,happy=hap,image=2,wc=wc)
        p.save()
        pid=p.pk
        return redirect('dashboard', pid)

    trend=twitterAPI.twitterTrends()
    return render(request,'search.html',{'trend':trend})

@login_required(login_url='login')
def dashboard(request,id):

    if request.method == "GET":
        request.session['id'] = id
        i=request.session['id']
        project = Project.objects.filter(user_id=request.user,pk=i).values_list()
        p = list(project)
        if len(p)==0:
            project = Project.objects.filter(user_id=request.user.id).values_list().first()
            p = list(project)
            pid = p[0]
            request.session['id'] = pid
            return redirect("projects")
    name = p[0][2]
    total = p[0][3]
    pos = p[0][4]
    neg = p[0][5]
    neu = p[0][6]
    hap = p[0][7]
    ang = p[0][8]
    img = p[0][9]
    wc = p[0][10]
    fn="C:\\Users\\M.FAIZAN\\tweetolytic\\tweetolytics\\static\\wordcloudoutput\\image.png"
    with open(fn, 'wb') as f:
        f.write(wc)
        f.close()
    labels = ['Positive', 'Negative', 'Neutral', 'Angry', 'Happy']
    # pos, neg, neu, ang,total, hap=2,6,3,6,3,6
    data=[pos,neg,neu,ang,hap]
    n = request.user.username
    context={'labels':labels,'name':name,'total':total,'data':data}
    return render(request,'dashboard.html',context)


@login_required(login_url='login')
def deleteProject(request,id):
    # print("deleee",id)
    if request.method=="GET":
        Project.objects.get(id=id).delete()
        p = Project.objects.filter(user_id=request.user.id)
        if p.count() == 0:
            return redirect("search")
        project=Project.objects.filter(user_id=request.user.id).values_list().first()
        p = list(project)
        pid=p[0]
        request.session['id'] = pid

        return redirect("projects")

    return render(request,'projects.html')

@login_required(login_url='login')
def projects(request):
    p=Project.objects.filter(user_id=request.user.id)
    if p.count()==0:
        return redirect("search")
    return render(request,'projects.html',{'projects':p})


# @login_required(login_url='login')
# def home(request):
#     # if request.method == "GET":
#     id=request.session['id']
#     # print('ffffffff',id)
#     #     project = Project.objects.filter(pk=id).values_list()
#     #     p = list(project)
#     # id=p[0][1]
#     # print("homeeeee",id)
#     # name = p[0][2]
#     return render(request,'dbase.html',{'pid':id})



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
def compare(request):
    if request.method == "GET":
        option = request.GET.get("option")
        print("pop", option)
        if option:
            project = Project.objects.filter(pk=option).values_list("positive")
            pp = list(project)
        pid=request.session['id']
        p = Project.objects.filter(user_id=request.user.id).exclude(pk=pid)

    return render(request, 'compare.html', {'projects': p})

def compareproject(request):
    if request.method=="GET":
        option = request.GET.get("option")
        if option:
            project = Project.objects.filter(pk=option).values_list()
            p = list(project)
            print("pop",p)
            return redirect("compare")
    return render(request, 'compare.html')