from django.urls import path
from . import views
urlpatterns=[path('login/',views.LoginPage,name="login"),
    path('register/',views.registerUser,name="register"),
    path('logout/',views.logoutUser,name="logout"),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create_room/', views.create_room, name="create_room"),
    path('update_room/<str:pk>/', views.update_Topic, name="update_room"),
    path('delete_room/<str:pk>/',views.delete_room,name='delete_room'),
    path('deleteques/<str:pk>/',views.deletequestion,name="deletequestion"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
    ]
