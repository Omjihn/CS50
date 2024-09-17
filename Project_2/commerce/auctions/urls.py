from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),

    path('listing/new', views.addListing, name='addListing'),
    path('listing/<int:id>/', views.showListing, name='showListing'),
    path('listing/<int:listing_id>/close/', views.close_listing, name='close_listing'),
    path('listing/<int:id>/watchlist/', views.watchlistSwitch),
    path('listing/<int:id>/bid/', views.addBid, name='addBid'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('search/', views.searchCategory, name='searchCategory'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
