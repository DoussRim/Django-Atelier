# from .forms import ModelForm
from django import forms
from .models import Event
from django.forms import Textarea
from datetime import date


class AddForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = ("__all__")
        # exclude=['state',]
        
        # image=forms.ImageField()
        fields=("title","description","event_date","image",
                "organizer","category")
        widgets={'description':Textarea(
            attrs={'cols':20,'rows':30}
        )},
        help_texts={
            'title':{'Your title here!'  ,}
        }
        error_messages={
            'title':{
                'max_length':"this event's title is too long",
            },
        }
    event_date=forms.DateField(label="Date de l'evt",
                                   initial=date.today,
                                   widget=forms.DateInput(
                                       attrs={'type':'date',
                                              'class':'form-control date-input'}
                                   )
                                   )
    category=forms.ChoiceField(
            label='Evt Category',
            widget=forms.RadioSelect,
            choices=Event.category_choices
        )
        
