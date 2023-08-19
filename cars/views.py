from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, IntegerField, CharField
from django.db.models.functions import Lower, Cast
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.conf import settings

from django.http import JsonResponse
from .models import Car, Make, Favorite, CarMake, CarModel, CarYear, CarMileage, CarTransmission, ContactMessage
from .forms import CarSelectionForm, CarForm, ContactForm

from django.urls import reverse_lazy


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

            if sortkey == 'year':
                # sortkey = 'lower_year'
                sortkey = 'year_text'
                # cars = cars.annotate(lower_year=Lower('year')
                cars = cars.annotate(year_text=Cast('year', CharField()))

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


# Contact Us

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                subject,
                f"From: {email}\n\n{message}",  
                email,  
                ['igor@sergutin.com'],
                fail_silently=False,
            )

            # send_mail(
            #     subject,
            #     message,
            #     from_email,
            #     ['igor@sergutin.com'],  
            #     fail_silently=False,
            # )

            messages.success(request, 'Your message has been sent. We will get back to you soon.')
            return redirect('contact')

    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'cars/contact.html', context)

# Cash for Cars

def get_car_models(request):
    make_id = request.GET.get('make_id')
    models = CarModel.objects.filter(make_id=make_id)
    model_list = [{"id": model.id, "name": model.name} for model in models]
    return JsonResponse(model_list, safe=False)


def get_car_years(request):
    model_id = request.GET.get('model_id')
    years = CarYear.objects.filter(model_id=model_id)
    year_list = [{"id": year.id, "year": year.year} for year in years]
    return JsonResponse(year_list, safe=False)


def get_car_mileages(request):
    year_id = request.GET.get('year_id')
    mileages = CarMileage.objects.filter(year_id=year_id)
    mileage_list = [{"id": mileage.id, "mileage": mileage.mileage} for mileage in mileages]
    return JsonResponse(mileage_list, safe=False)


def get_car_transmissions(request):
    mileage_id = request.GET.get('mileage_id')
    transmissions = CarTransmission.objects.filter(mileage_id=mileage_id)
    transmission_list = [{"id": transmission.id, "transmission": transmission.transmission} for transmission in transmissions]
    return JsonResponse(transmission_list, safe=False)


def car_selection_view(request):
    if request.method == 'POST':
        form = CarSelectionForm(request.POST)
        if form.is_valid():
            selected_make = form.cleaned_data['car_make']
            selected_model = form.cleaned_data['car_model']
            selected_year = form.cleaned_data['car_year']
            selected_mileage = form.cleaned_data['car_mileage']
            selected_transmission = form.cleaned_data['car_transmission']
            selected_engine = form.cleaned_data['car_engine']

    else:
        form = CarSelectionForm()

    context = {'form': form}
    return render(request, 'cash.html', context)
