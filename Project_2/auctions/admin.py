from django.contrib import admin

from .models import Comment, Bid, Listing, Watchlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_price', 'current_price', 'level', 'user', 'creation_date')
    search_fields = ('title', 'description')
    ordering = ('-creation_date',)
    fields = ('user', 'title', 'description', 'starting_price', 'current_price', 'level', 'picture', 'closed')


class BidAdmin(admin.ModelAdmin):
    list_display = ('listing_title', 'content', 'price', 'user', 'creation_date')
    search_fields = ('listing_title', 'content')
    ordering = ('-creation_date',)
    fields = ('user', 'listing', 'content', 'price')

    def listing_title(self, obj):
        return obj.listing.title
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing_title', 'content', 'user', 'creation_date')
    search_fields = ('listing_title', 'user')
    ordering = ('-creation_date',)
    fields = ('user', 'listing', 'content',)

    def listing_title(self, obj):
        return obj.listing.title

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('listing_title', 'user', 'creation_date')
    search_fields = ('listing_title', 'user')
    ordering = ('-creation_date',)
    fields = ('user', 'listing')

    def listing_title(self, obj):
        return obj.listing.title

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
