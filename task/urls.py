from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.loginpage,name='login'),
    path('register/',views.registerpage,name='register'),
    path('home/',views.home,name='home'),
    path('ml/',views.ml,name='ml'),
    path('logout/',views.logout,name='logout')
]