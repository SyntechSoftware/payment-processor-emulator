from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model


class BillingParams(models.Model):
    supplier = models.OneToOneField(get_user_model())
    success_url = models.CharField(max_length=255, default='/done/',
                                      help_text="Redirect to url, if iframe processing is success")
    failure_url=models.CharField(max_length=255, default='/done/',
                                      help_text="Redirect to url, if iframe processing is faild")
    transaction_password=models.CharField(max_length=255, blank=True, null=True,
                                      help_text="Can be received as TranzilaPW-field in request. Checking if present")
    include_cc = models.BooleanField(default=False,
                                      help_text="Return full Card number in iframe response if enabled, "
                                                "or last 4 digits else")
    generate_errors = models.BooleanField(default=True,
                                      help_text="If enabled - system return random errors during processing")


class Transaction(models.Model):
    supplier = models.ForeignKey(get_user_model())
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    ccno = models.CharField(max_length=20)
    Response = models.CharField(max_length=5)
    TranzilaTK = models.CharField(max_length=20)
    Tempref = models.CharField(max_length=10)
    ConfirmationCode = models.CharField(max_length=10)
    benid = models.CharField(max_length=40)
    sum = models.FloatField()
    csum = models.FloatField(default=0.0)
    dsum = models.FloatField(default=0.0)
    expmonth = models.CharField(max_length=4)
    expyear = models.CharField(max_length=4)
    expdate = models.CharField(max_length=6)
    cred_type = models.CharField(max_length=5)
    currency = models.IntegerField()
    cardtype = models.IntegerField()
    cardissuer = models.IntegerField()                  # 1-9
    cardaquirer = models.IntegerField()
    lang = models.CharField(max_length=5)
    myid = models.CharField(max_length=5)
    Responsesource = models.IntegerField(default=0)     # == 0 if True
    Responsecvv = models.IntegerField(default=0)        # == 1 or 3 if True
    Responseid = models.IntegerField(default=0)         # > 0 if True
    params = models.TextField(default='{}')


class Tokenization(models.Model):
    token = models.CharField(max_length=20, db_index=True, primary_key=True)
    supplier = models.ForeignKey(get_user_model())
    ccno = models.CharField(max_length=20, db_index=True)


CURRENCIES = {
    '1': 'LIS',
    '2': 'USD',
    '3': 'GBP',
    '4': 'NIS',
    '5': 'HKD',
    '6': 'JPY',
    '7': 'EUR',
    '8': 'OTH'
}

TRANSACTION_MODES = {
    'A': 'Remote Approved',
    'M': 'Local Approved',
    'V': 'Remote Verified',
    'Y': 'Local Verified',
    'F': 'Forcing Transaction',
    'C': 'Credit Transaction'
}
