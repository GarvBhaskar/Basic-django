from django.shortcuts import render,redirect,HttpResponse
from .models import Topic,Room,Questions
from .forms import TopicForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect("home")
    if(request.method=="POST"):
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"Invalid username")
        user=authenticate(request,username=username, password=password)
        if user!= None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not Exist")
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    page='register'
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error while registration")

    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def userProfile(request, pk):
    user=User.objects.get(id=pk)
    room=Room.objects.filter(id=pk)
    topics=Topic.objects.filter(host=pk)
    topic_messages=Questions.objects.filter(user=user).distinct()
    context={'user':user, 'topics':topics, "room":room, 'room_messages': topic_messages}
    return render(request, 'base/profile.html', context)

def home(request):
    #getting data from the models which stores the tables
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    room=Room.objects.all()
    if(q!="C"):
        topics=Topic.objects.filter(
            Q(room__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))#icontains is case insensitive
    else:
        topics=Topic.objects.filter(
            Q(room__name__icontains=q)
        )
    topic_count=topics.count()
    topic_messages=Questions.objects.filter(Q(topic__room__name__icontains=q))
    context={'topics':topics,'room':room,'tcount':topic_count, 'room_messages': topic_messages}
    print(topics)
    return render(request, 'base/home.html',context)

def room(request,pk):
    topic=Topic.objects.get(id=pk)
    questions=topic.questions_set.all().order_by("-created")
    participants=topic.participants.all()
    if request.method=='POST':
        ques=Questions.objects.create(
            user=request.user,
            topic=topic,
            body=request.POST.get('body')
        )
        topic.participants.add(request.user)
        return redirect('room', pk=topic.id)
    context={'topics':topic,"questions":questions,"participants":participants}
    return render(request, 'base/room.html',context)


@login_required(login_url='login')
def create_room(request):
    form=TopicForm()
    #we can see the data being sent and save it
    if request.method =='POST':
        form=TopicForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host= request.user
            room.save()
            return redirect('home')
    context={'form':form,}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_Topic(request,pk):
    topic=Topic.objects.get(id=pk)
    form=TopicForm(instance=topic)
    if request.user!= topic.host :
        return HttpResponse("You are not the creator of this room!")
    if(request.method=='POST'):
        form=TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    topic=Topic.objects.get(id=pk)
    if request.user!= topic.host :
        return HttpResponse("You are not the creator of this room!")
    if (request.method=='POST'):
        topic.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':topic})

@login_required(login_url='login')
def deletequestion(request,pk):
    ques=Questions.objects.get(id=pk)
    if request.user!= ques.user :
        return HttpResponse("You are not the creator of this room!")
    if (request.method=='POST'):
        ques.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':ques})