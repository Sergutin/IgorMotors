from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.deletion import CASCADE


class Make(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Car(models.Model):
    category = models.ForeignKey('Make', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# Favorite


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.car.name}"


# Contact Us

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


# Cash for Cars feature

class CarMake(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarYear(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class CarMileage(models.Model):
    year = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    mileage = models.PositiveIntegerField()

    def __str__(self):
        return str(self.mileage)


class CarTransmission(models.Model):
    mileage = models.ForeignKey(CarMileage, on_delete=models.CASCADE)
    transmission = models.CharField(max_length=20)

    def __str__(self):
        return self.transmission


class CarEngine(models.Model):
    transmission = models.ForeignKey(CarTransmission, on_delete=models.CASCADE)
    engine = models.CharField(max_length=20)

    def __str__(self):
        return self.engine
