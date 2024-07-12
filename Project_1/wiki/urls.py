from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="name"),
    path("<str:name>/", views.page, name="page"),
]