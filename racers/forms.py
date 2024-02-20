from django import forms
from .models import Racer, Group
from .models import LapTime

class LapTimeForm(forms.ModelForm):
    class Meta:
        model = LapTime
        fields = ['racer', 'lap_time', 'lap_number']
        widgets = {
            'racer': forms.HiddenInput(),
            'lap_time': forms.TextInput(attrs={'class': 'form-control lap-time-input'}),
            'lap_number': forms.HiddenInput(),
        }


class RacerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['rider_number', 'name', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rider_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RacerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.none()

        if 'category' in self.data:
            try:
                category = self.data.get('category')
                self.fields['group'].queryset = Group.objects.filter(category=category).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Group queryset

from django import forms
from django.forms import modelformset_factory
from .models import RaceModeData, Racer, Group

class RaceModeDataForm(forms.ModelForm):
    class Meta:
        model = RaceModeData
        fields = ['racer', 'group', 'finish_position', 'penalty']
        widgets = {
            'racer': forms.HiddenInput(),
            'group': forms.HiddenInput(),
            'finish_position': forms.Select(choices=[
                ('N/A', 'N/A'),
                ('P1', 'P1'),
                ('P2', 'P2'),
                ('P3', 'P3'),
                ('P4', 'P4'),
                ('P5', 'P5'),
                ('P6', 'P6'),
                ('DNF', 'DNF'),
            ], attrs={'class': 'form-control'}),
            'penalty': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Creating a formset for RaceModeData
RaceModeDataFormSet = modelformset_factory(
    RaceModeData,
    form=RaceModeDataForm,
    extra=0,  # No extra forms
    can_delete=True,  # Allow deletion
)
