from django import forms

from bookmaker.models import Bet, UserBet


class CreateBetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['bet_text', 'resolve_date']
        widgets = {
            'bet_text': forms.Textarea(attrs={'class': 'form-control'}),
            'resolve_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class UserBetForm(forms.ModelForm):
    class Meta:
        model = UserBet
        fields = ['wagered_amount', 'wagered_option']
        widgets = {
            'wagered_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'wagered_option': forms.Select(attrs={'class': "form-control"}),
        }
