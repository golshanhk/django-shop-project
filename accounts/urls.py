from . import views
from django.urls import path

app_name='accounts'
urlpatterns =[
    path('register/',views.user_register , name="user_register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/',views.user_profile, name='profile'),
    path('Update/',views.user_update_profile, name='Update'),
    path('change_password/',views.change_password,name='change_password'),
]