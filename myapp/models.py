from django.db import models
from django.utils import timezone

# Create your models here.
          
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mno = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=20)
    profile = models.ImageField(default="")     
    usertype = models.CharField(max_length=20 ,default="Customer")             
    
    def __str__(self):
        return f"{self.name}"
    
class Courses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cname = models.CharField(max_length=100)
    cprice = models.IntegerField()
    desc = models.TextField()
    cimage = models.ImageField(default="")
    duration = models.IntegerField()
    tname = models.CharField(max_length=100)
    texp = models.CharField(max_length=20)
    timage = models.ImageField(default="")                             
    
    def __str__(self):
        return f"{self.cname}"

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses,on_delete=models.CASCADE)
    ttime = models.DateTimeField(default=timezone.now)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses,on_delete=models.CASCADE)
    ttime = models.DateTimeField(default=timezone.now)
    tprice = models.IntegerField()
    qty = models.IntegerField(default=1)
    payment = models.BooleanField(default=False)
    
    