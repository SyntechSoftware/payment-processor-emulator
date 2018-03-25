from django.forms import ModelForm, PasswordInput
from .models import BillingParams


class BillingParamsForm(ModelForm):
    class Meta:
        model = BillingParams
        fields = ['supplier', 'success_url', 'failure_url', 'transaction_password', 'include_cc', 'generate_errors']
        exclude = ['supplier']
        widgets = {
            'transaction_password': PasswordInput(),
        }
