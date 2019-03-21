from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Codes(models.Model):
    '''
    Table For Tax Codes
    '''

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=70, null=True, blank=True)
    tax_pct = models.DecimalField(max_digits=6, decimal_places=4, null=False)
    tax_pct_2 = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    is_refundable = models.BooleanField(default=False)
    non_taxable_limit = models.DecimalField(max_digits=20, decimal_places=4, default=0, null=False)

class Users(models.Model):
    '''
    Table For Users
    '''
    name = models.CharField(max_length=70, null=True, blank=True)


class Items(models.Model):
    '''
    Table For Tax Items
    '''
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    code = models.ForeignKey(Codes, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

