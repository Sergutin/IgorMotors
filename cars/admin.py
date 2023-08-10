from django.contrib import admin
from .models import Car, Make

# Register your models here.


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


admin.site.register(Car, CarAdmin)
admin.site.register(Make, MakeAdmin)
