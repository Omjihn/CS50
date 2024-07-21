from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('listing/new', views.addListing, name='addListing'),
    path('listing/<int:id>/', views.showListing, name='showListing')
]
