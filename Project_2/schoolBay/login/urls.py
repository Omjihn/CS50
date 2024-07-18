from django.urls import path

from . import views

urlpatterns = [
    path('', views.user, name='user'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view , name='login')
]
