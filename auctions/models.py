from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now=True)
    
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    # choices for the category of the listing
    CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('HOME', 'Home'),
        ('FASHION', 'Fashion'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(max_length=32, choices=CHOICES, default='OTHER')
    image = models.URLField()
    time = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)