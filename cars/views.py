from django.shortcuts import render
from .models import Car

# Create your views here.

def all_cars(request):
    """ A view to show all cars """

    cars = Car.objects.all()

    context = {
        'cars': cars,
    }

    return render(request, 'cars/cars.html', context)