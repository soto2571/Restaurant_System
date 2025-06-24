from django import forms
from .models import OrderNote, Account

class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNote
        fields = ['item']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['customer_name']