from decimal import Decimal, InvalidOperation

from django import forms
from django.core.exceptions import ValidationError


class AddBalanceForm(forms.Form):
    PRESET_AMOUNTS = (
        (Decimal('100000'), '100 000'),
        (Decimal('200000'), '200 000'),
        (Decimal('500000'), '500 000'),
        (Decimal('1000000'), '1 000 000'),
    )

    preset_amount = forms.ChoiceField(
        choices=(('', 'Custom'),) + PRESET_AMOUNTS,
        required=False,
        widget=forms.RadioSelect,
    )
    custom_amount = forms.DecimalField(
        required=False,
        min_value=Decimal('1'),
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Custom amount', 'min': '1'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        preset_amount = cleaned_data.get('preset_amount')
        custom_amount = cleaned_data.get('custom_amount')

        if preset_amount:
            try:
                amount = Decimal(str(preset_amount))
            except InvalidOperation as exc:
                raise ValidationError('Invalid preset amount.') from exc
        else:
            amount = custom_amount

        if amount is None or amount <= 0:
            raise ValidationError('Amount must be positive.')

        cleaned_data['amount'] = amount
        return cleaned_data
