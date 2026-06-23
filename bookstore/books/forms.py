from django import forms
from .models import Book
from .models import Address

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'image', 'description','stock','category']

#地址表单
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['receiver_name', 'phone', 'province', 'city', 'district', 'detail', 'postal_code', 'is_default']