from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, F, IntegerField
from django.db.models.functions import Lower

from .models import Car, Make
from .forms import CarForm

# Create your views here.

def all_cars(request):
    """ A view to show all cars """

    cars = Car.objects.all()
    query = None
    makes = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                cars = cars.annotate(lower_name=Lower('name'))

            if sortkey == 'make':  
                sortkey = 'make_name'
                cars = cars.annotate(make_name=F('category__name'))

            # if sortkey == 'category':
            #     sortkey = 'category__name'

            if sortkey == 'year':
                sortkey = 'lower_year'
                cars = cars.annotate(lower_year=Lower('year'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            cars = cars.order_by(sortkey)


        if 'make' in request.GET:
            makes = request.GET['make'].split(',')
            cars = cars.filter(category__name__in=makes)
            makes = Make.objects.filter(name__in=makes)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('cars'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            cars = cars.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'cars': cars,
        'search_term': query,
        'current_makes': makes,
        'current_sorting': current_sorting,
    }

    return render(request, 'cars/cars.html', context)


def car_detail(request, car_id):
    """ A view to show individual car details """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }

    return render(request, 'cars/car_detail.html', context)

def add_car(request):
    """ Add a car to the store """
    form = CarForm()
    template = 'cars/add_car.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
