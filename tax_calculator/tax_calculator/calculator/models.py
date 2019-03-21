from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Codes(models.Model):
    '''
    Table For Tax Codes
    '''

    id = models.IntegerField(primary_key=True)
    tax_pct = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    is_refundable = models.BooleanField(default=False)
    non_taxable_limit = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

class Items(models.Model):
    '''
    Table For Tax Items
    '''

    tax_code = models.ForeignKey(Codes, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

class Bills(models.Model):
    '''
    Table For Tax Bills
    '''

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=4, null=True)

