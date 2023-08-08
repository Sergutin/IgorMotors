from django.shortcuts import render, get_object_or_404
from .models import Car

# Create your views here.

def all_cars(request):
    """ A view to show all cars """

    cars = Car.objects.all()

    context = {
        'cars': cars,
    }

    return render(request, 'cars/cars.html', context)


def car_detail(request, car_id):
    """ A view to show individual car details """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }

    return render(request, 'cars/car_detail.html', context)