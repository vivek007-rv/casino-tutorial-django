from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount',
            'step': '0.01'
        }),
        help_text='Enter the amount you want to deposit (minimum $0.01)',
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount > Decimal('10000.00'):
            raise forms.ValidationError('Maximum deposit amount is $10,000')
        return amount
