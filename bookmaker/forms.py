from django import forms

from bookmaker.models import Bet


class CreateBetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['bet_text', 'resolve_date', 'possible_to_draw']
        widgets = {
            'bet_text': forms.Textarea(attrs={'class': 'form-control'}),
            'resolve_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'possible_to_draw': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
