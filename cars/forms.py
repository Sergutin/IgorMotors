from django import forms
from .widgets import CustomClearableFileInput
from .models import Car, Make
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


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(label=_('Email'), required=True)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'rows': 5}), required=True)
