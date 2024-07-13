from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="name"),
    path("random/", views.getRandom),
    path("<str:name>/", views.page, name="page"),
    path("<str:name>/edit", views.editPage, name="page"),
]