# -*- coding: utf-8 -*-

"""Project forms"""

# Global imports:
from django import forms

# Local imports:
from models import ElectionResult

date_choices = [ ( date['date'].isoformat(), date['date'].isoformat() )
                for date in ElectionResult.objects.all().values('date').distinct().order_by('date') ]

class ElectionForm(forms.Form):

    date = forms.ChoiceField(
        label = 'Eleição de ',
        choices = date_choices,
       )

    uni = forms.ChoiceField(
        label = 'Distribuição por',
        choices = (
            ( 'M', 'círculos eleitorais' ),
            ( 'U', 'um circulo eleitoral único' )
            ),
       )

    seats = forms.IntegerField(
            label = 'Assentos',
            min_value = 10,
            max_value = 1000,
            )
