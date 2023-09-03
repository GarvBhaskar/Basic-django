from django.urls import path
from . import views

urlpatterns=[
    path('hello/', views.sayHello,name='hello')
    ,path('',views.home, name="Home"),
    path('bye/',views.bye)
]
