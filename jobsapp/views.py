from django.shortcuts import render, redirect
from django.contrib import messages
from jobsapp.models import *
import bcrypt


# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    return render(request, 'index.html')

def register(request):
    error = User.objects.regValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user=User.objects.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['email'], password=pw_hash)
    request.session['user']=user.id
    return redirect('/dashboard')

def login(request):
    error = User.objects.loginValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user']=user.id
    return redirect('/dashboard')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user'])
    jobs = Job.objects.all()
    taken = Job.objects.filter(employee=None)
    print(taken)
    context={
        'user': current_user,
        'jobs': jobs,
        'user_jobs': Job.objects.filter(employee=current_user),
        'taken':taken
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    del request.session['user']
    return redirect('/')

def new(request):
    user = User.objects.get(id=request.session['user'])
    context={
        'user':user
    }
    return render(request, 'new.html',context)

def add_new(request):
    error = User.objects.infoValidator(request.POST)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='info')
        return redirect('/jobs/new')
    creator = User.objects.get(id=request.session['user'])
    Job.objects.create(title=request.POST['title'], location=request.POST['location'], desc=request.POST['desc'], creator=User.objects.get(id=request.session['user']))
    return redirect('/dashboard')

def add_job(request, id):
    user = User.objects.get(id=request.session['user'])
    job = Job.objects.get(id=id)
    if job.employee:
        return redirect('/dashboard')
    user.jobs.add(job)
    return redirect('/dashboard')

def remove_job(request,id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('/dashboard')

def job_info(request, id):
    user=User.objects.get(id=request.session['user'])
    job = Job.objects.get(id=id)
    # user_in_job = job.filter(employee=user)
    context ={
        'user':user,
        'job':job,
        # 'user_in_job': user_in_job

    }
    return render(request, 'job_info.html', context)

def give_up(request,id):
    user=User.objects.get(id=request.session['user'])
    job = Job.objects.get(id=id)
    user.jobs.remove(job)
    return redirect('/dashboard')

def done(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('/dashboard')

def edit(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    context={
        'job':job,
        'user':user
    }
    return render(request, 'edit.html', context)

def edit_job(request, id):
    error = User.objects.editValidator(request.POST)
    job = Job.objects.get(id=id)
    if len(error)>0:
        for key, value in error.items():
            messages.error(request, value, extra_tags='edit')
        return redirect('/jobs/edit/'+str(id))
    job.title= request.POST['title']
    job.desc = request.POST['desc']
    job.location=request.POST['location']
    job.save()
    return redirect('/dashboard')