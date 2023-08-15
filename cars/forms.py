from django import forms
from .models import Car, Make


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        makes = Make.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in makes]

        self.fields['make'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
