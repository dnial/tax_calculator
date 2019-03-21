from tax_calculator.calculator.models import Codes, Items, Users


def create_user(name=""):
    user = Users(name=name)
    user.save()
    return user


def create_item(user=None, name="", code=None, price=None):        
    code = Codes.objects.get(id=code)

    item = Items(code=code, user=user, name=name, price=price)
    item.save()
    return item

def calculate_bills(user=None):
    items = Items.objects.filter(user=user)
    bills = []
    price_subtotal = 0
    tax_subtotal = 0

    for item in items:
        tax, amount = calculate_tax(item)
        bill = {
            "Name": item.name,
            "Tax Code": item.code.id,
            "Type": item.code.name,
            "Refundable": "Yes" if item.code.is_refundable else "No",
            "Price": item.price,
            "Tax": tax,
            "Amount": amount
        }
        price_subtotal += item.price
        tax_subtotal += tax
        bills.append(bill)
    
    data = {
        "Bills": bills, 
        "Price Subtotal": price_subtotal,
        "Tax Subtotal": tax_subtotal,
        "Grand Total": price_subtotal + tax_subtotal,
    }
    return data

def calculate_tax(item=None):
    code = item.code
    price = item.price

    taxable_price = price-code.non_taxable_limit
    tax_amount = taxable_price * code.tax_pct + (taxable_price * code.tax_pct_2 if code.tax_pct_2 else 0)
    total = price + tax_amount

    return tax_amount, total
