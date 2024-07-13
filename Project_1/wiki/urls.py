from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="name"),
    path("search/", views.searchIndex),
    path("random/", views.getRandom),
    path("new/", views.newPage),
    path("<str:name>/", views.page, name="page"),
    path("<str:name>/edit", views.editPage, name="page"),
]