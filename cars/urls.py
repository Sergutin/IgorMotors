from django.urls import path, include
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('', views.all_cars, name='cars'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    path('add/', views.add_car, name='add_car'),
    path('edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('favorites/', views.view_favorites, name='favorites'),
    path('add_to_favorites/<int:car_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:car_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('contact/', views.contact, name='contact'),
    path('cash/', views.car_selection_view, name='cash'),
    path('get_car_models/', views.get_car_models, name='get_car_models'),
    path('get_car_years/', views.get_car_years, name='get_car_years'),
    path('get_car_mileages/', views.get_car_mileages, name='get_car_mileages'),
    path('get_car_transmissions/', views.get_car_transmissions, name='get_car_transmissions'),
    path('get_car_engines/', views.get_car_engines, name='get_car_engines'),
    # path('car_selection_view/', views.car_selection_view, name='car_selection_view'),

]
