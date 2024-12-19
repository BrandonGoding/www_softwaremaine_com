import requests
from django.conf import settings
from django.shortcuts import render
from requests.exceptions import RequestException

from .forms import GiftCardBalanceForm


def gift_card_modal(request):
    """Serve the gift card balance form for the modal."""
    form = GiftCardBalanceForm()
    return render(
        request, "website/partials/gift_card_form_partial.html", {"form": form}
    )


def gift_card_balance(request):
    """Process the gift card balance check."""
    if request.method != "POST":
        return render(
            request,
            "website/partials/gift_card_form_partial.html",
            {"form": GiftCardBalanceForm()},
        )

    form = GiftCardBalanceForm(request.POST)
    balance, error = None, None

    if form.is_valid():
        gift_card_number = form.cleaned_data["gift_card_number"]
        headers = {
            "Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {"gan": gift_card_number}

        try:
            response = requests.post(
                f"{settings.SQUARE_API_URL}/from-gan", json=payload, headers=headers
            )
            response.raise_for_status()

            data = response.json()
            amount = data.get("gift_card", {}).get("balance_money", {}).get("amount", 0)
            balance = "${:,.2f}".format(amount / 100 if amount else 0)
        except RequestException:
            error = "An error occurred while retrieving the gift card balance. Please try again later."
        except KeyError:
            error = "Unexpected response format from the API."
    else:
        error = "Invalid input. Please check your gift card number."

    return render(
        request,
        "website/partials/gift_card_balance_result.html",
        {"form": form, "balance": balance, "error": error},
    )
