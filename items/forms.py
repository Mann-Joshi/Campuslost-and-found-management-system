from django import forms

from .models import ItemReport


class ItemReportForm(forms.ModelForm):
    class Meta:
        model = ItemReport
        fields = ['item_type', 'name', 'description', 'location']
