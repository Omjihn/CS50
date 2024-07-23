from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('listing/new', views.addListing, name='addListing'),
    path('listing/<int:id>/', views.showListing, name='showListing'),
     path('listing/<int:listing_id>/close/', views.close_listing, name='close_listing'),
    path('listing/<int:id>/watchlist/', views.watchlistSwitch),
    path('listing/<int:id>/bid/', views.addBid, name='addBid'),
    path('watchlist/', views.watchlist, name='watchlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
