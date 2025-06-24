from django import forms
from .models import OrderNote, Account

class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNote
        fields = ['account', 'item']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['table', 'customer_name']