from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True)
    isBuyer = models.BooleanField(default=True)
    def __str__(self):
        return f"({self.phone} {self.last_name})"
class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    userId=models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.TextField(null=True)
    status=models.BooleanField(default=False)
    brokerage=models.BooleanField(default=False)
    price=models.IntegerField()
    city=models.CharField(max_length=20)
    neighborhood=models.CharField(max_length=20)
    street=models.CharField(max_length=20)
    houseNumber=models.IntegerField()
    floor=models.IntegerField()
    rooms=models.IntegerField()

    def __str__(self):
        return f"({self.id} {self.userId}{self.description}{self.status}{self.brokerage}{self.city}{self.neighborhood}{self.street}{self.houseNumber}{self.floor}{self.rooms})"
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image=models.ImageField(upload_to='images/', null=True, blank=True)
    apartmentId = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    def __str__(self):
        return f"({self.id} {self.image})"



class message(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField()
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    apartmentId = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    def __str__(self):
        return f"({self.id} {self.body} {self.apartmentId})"