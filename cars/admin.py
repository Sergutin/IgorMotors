from django.contrib import admin
from .models import Car, Make, ContactMessage, CarMake, CarModel
from django.apps import AppConfig



class CarAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image',
        'year', # Added for year sorting test
    )
    ordering = ('sku',)


class MakeAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('subject', 'name', 'email')


class CustomCarsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_cars_app'  
    verbose_name = 'Custom Car Management' 

admin.site.register(Car, CarAdmin)
admin.site.register(Make, MakeAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(CarMake)
admin.site.register(CarModel)
