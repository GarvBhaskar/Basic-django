from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

contents=[{'id':'1','Work':'Work 1'},{'id':'2','Work':'Work 2'},]

def home(request):
    return render(request,'playground/Home.html',{'contents':contents})
def sayHello(request):
    return render( request, 'playground/hello.html')
def bye(request):
    return render(request,'playground/Bye.html')
