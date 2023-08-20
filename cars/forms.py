from django import forms
from .widgets import CustomClearableFileInput
from .models import Car, Make, CarMake, CarModel, CarYear, CarMileage, CarTransmission, CarEngine
from django.utils.translation import gettext_lazy as _


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        makes = Make.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in makes]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

# Contact Us

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(label=_('Email'), required=True)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'rows': 5}), required=True)

# Cash for Cars

class CarSelectionForm(forms.Form):
    car_make = forms.ModelChoiceField(queryset=CarMake.objects.all() | CarMake.objects.filter(name__in=[]), empty_label="Select Make")
    car_model = forms.ChoiceField(choices=[], required=True)
    car_year = forms.ChoiceField(choices=[], required=True)
    car_mileage = forms.ChoiceField(choices=[], required=True)
    car_transmission = forms.ChoiceField(choices=[], required=True)
    car_engine = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_model'].widget.attrs.update({'class': 'form-control'})
        self.fields['car_year'].widget.attrs.update({'class': 'form-control'})
        self.fields['car_mileage'].widget.attrs.update({'class': 'form-control'})
        self.fields['car_transmission'].widget.attrs.update({'class': 'form-control'})
        self.fields['car_engine'].widget.attrs.update({'class': 'form-control'})
