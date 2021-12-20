
from django import forms
from .models import shop_products


# creating a form

class product_filter_form(forms.ModelForm):
    
    sort_order = forms.ChoiceField(choices=[('Recommended','recommended'), ('SortAscending','sort-ascending'),('SortDescending','sort-descending')], required=False)
    shop_product_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Product Name'}))
    class Meta:
        model = shop_products
        fields = ['shop_product_name', 'category', 'sort_order']
        widgets = {
        'category': forms.Select(),
    }

    def __init__(self, *args, **kwargs):
        super(product_filter_form, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields['shop_product_name'].required = False
            self.fields['category'].required = False
            self.fields['sort_order'].required = False
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })