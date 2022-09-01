from django.urls import path

from todo import views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loginpage/', views.loginPage, name='loginPage'),
    path('registerpage/', views.registerPage, name='registerPage'),
    path('logoutpage/', views.logoutPage, name='logoutPage'),
    path('taskcreate/', views.createTask, name='taskCreate'),
    path('taskdelete/<item_id>/', views.remove, name='taskdelete'),
    path('taskupdate/<item_id>/', views.update, name='taskupdate'),
   
]
