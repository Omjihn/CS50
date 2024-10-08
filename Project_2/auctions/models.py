from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class   Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    starting_price = models.DecimalField(max_digits=24, decimal_places=2)
    current_price = models.DecimalField(max_digits=24, decimal_places=2, default=0)
    picture = models.URLField(max_length=2048)
    level = models.CharField(max_length=4)
    closed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

class   Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=24, decimal_places=2)
    content = models.CharField(max_length=2048)
    creation_date = models.DateTimeField(auto_now_add=True)

class   Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

class   Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
