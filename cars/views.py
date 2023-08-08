from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Car

# Create your views here.

def all_cars(request):
    """ A view to show all cars """

    cars = Car.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('cars'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            cars = cars.filter(queries)

    context = {
        'cars': cars,
        'search_term': query,
    }

    return render(request, 'cars/cars.html', context)


def car_detail(request, car_id):
    """ A view to show individual car details """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }

    return render(request, 'cars/car_detail.html', context)