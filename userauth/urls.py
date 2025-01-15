from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup, name='signup'),
    path('loginn/', views.loginn, name='login'),
    path('logoutt/', views.logoutt, name='logout'),
    path('upload', views.upload, name='upload'),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),
    path('explore/', views.explore),
    path('profile/<str:id_user>', views.profile),
    path('follow', views.follow, name='follow'),
    path('search-results/', views.search_results, name='search-results'),
    path('delete/<str:id>', views.delete),
]