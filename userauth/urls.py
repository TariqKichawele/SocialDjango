from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginn, name='login'),
    path('logout/', views.logoutt, name='logout'),
    path('upload', views.upload, name='upload'),
]