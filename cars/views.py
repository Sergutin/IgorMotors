from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, IntegerField
from django.db.models.functions import Lower

from .models import Car, Make, Favorite
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


@login_required
def add_car(request):
    """ Add a car to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, 'Successfully added car!')
            return redirect(reverse('car_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to add car. Please ensure the form is valid.')
    else:
        form = CarForm()
        
    template = 'cars/add_car.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_car(request, car_id):
    """ Edit a car in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated car!')
            return redirect(reverse('car_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to update car. Please ensure the form is valid.')
    else:
        form = CarForm(instance=car)
        messages.info(request, f'You are editing {car.name}')

    template = 'cars/edit_car.html'
    context = {
        'form': form,
        'car': car,
    }

    return render(request, template, context)

@login_required
def delete_car(request, car_id):
    """ Delete a car from the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    car = get_object_or_404(Car, pk=car_id)
    car.delete()
    messages.success(request, 'Car deleted!')
    return redirect(reverse('cars'))


@login_required
def add_to_favorites(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    Favorite.objects.get_or_create(user=request.user, car=car)
    messages.success(request, 'Car added to favorites!')
    return redirect('car_detail', car_id=car_id)


@login_required
def remove_from_favorites(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    Favorite.objects.filter(user=request.user, car=car).delete()
    messages.success(request, 'Car removed from favorites.')
    # return redirect('car_detail', car_id=car_id)
    return redirect('favorites')


@login_required
def view_favorites(request):
    """ A view to show user's favorite cars """

    favorites = Favorite.objects.filter(user=request.user)  
    favorite_cars = [favorite.car for favorite in favorites]

    context = {
        'favorite_cars': favorite_cars,
    }

    return render(request, 'cars/favorites.html', context)
