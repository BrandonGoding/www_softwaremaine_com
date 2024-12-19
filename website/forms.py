from django import forms
from django.core.exceptions import ValidationError


class GiftCardBalanceForm(forms.Form):
    gift_card_number = forms.CharField(
        label="Gift Card Number",
        max_length=16,
        widget=forms.TextInput(attrs={"placeholder": "Enter your gift card number"}),
    )

    def clean_gift_card_number(self):
        gift_card_number = self.cleaned_data.get("gift_card_number")
        if not gift_card_number.isdigit():
            raise ValidationError("The gift card number must be numeric.")
        return gift_card_number
