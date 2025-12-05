from django import forms
from .models import conference


class ConferenceModel(forms.ModelForm):
    class Meta:
        model=conference
        fields=['title','description','location','start_date', 'end_date']
        labels={
            'title':"nom de la conference",
            'description':"description",
            'location':"Location",
            'start_date':"date de debut de la conference",
            'end_date':"date de fin de la conferenece"
        }
        widgets={
            'title':forms.TextInput(
                attrs={
                    'placeholder':"ex conference"
                }
            ),
            'start_date' :forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de debut"
                }

            ), # type: ignore
            'end_date' :forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de debut"
                }
            ) # type: ignore
        }

        