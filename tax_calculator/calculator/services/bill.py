from django.core.exceptions import ObjectDoesNotExist

from calculator.models import Codes, Items, Users
from calculator.services import item as item_services
from calculator.services import user as user_services


def calculate_bills(user_id=None):

    try:
        user_data = user_services.get_user(user_id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User Id {} not found".format(user_id))

    items = item_services.get_items_by_user(user=user_data)
    bills = []
    price_subtotal = 0
    tax_subtotal = 0

    for item in items:
        tax, amount = calculate_tax(item)
        bill = {
            "name": item.name,
            "tax_code": item.code.id,
            "tax_type": item.code.name,
            "refundable": item.code.is_refundable,
            "refundable_txt": "Yes" if item.code.is_refundable else "No",
            "price": item.price,
            "price_txt": "{:.2f}".format(item.price),
            "tax": tax,
            "amount": amount
        }
        price_subtotal += item.price
        tax_subtotal += tax
        bills.append(bill)

    grand_total = price_subtotal + tax_subtotal
    data = {
        "bills": bills,
        "price_subtotal": price_subtotal,
        "price_subtotal_txt": "{:.2f}".format(price_subtotal),
        "tax_subtotal": tax_subtotal,
        "tax_subtotal_txt": "{:.2f}".format(tax_subtotal),
        "grand_total": grand_total,
        "grand_totaltxt": "{:.2f}".format(grand_total),
    }
    return data


def calculate_tax(item=None):
    code = item.code
    price = item.price

    taxable_price = price - code.non_taxable_limit
    tax_amount = taxable_price * code.tax_pct + (taxable_price * code.tax_pct_2 if code.tax_pct_2 else 0)
    total = price + tax_amount

    return tax_amount, total
