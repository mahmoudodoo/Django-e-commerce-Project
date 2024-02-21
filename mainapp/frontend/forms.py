from django import forms




class ShippingAddressForm(forms.Form):
   street_address = forms.CharField(widget=forms.TextInput(attrs={
       'class': 'form-control',
       'id': 'floatingInput',
       'placeholder': 'Street and house number'
   }))


   apartment_address = forms.CharField(widget=forms.TextInput(attrs={
       'class': 'form-control',
       'id': 'floatingApartment',
       'placeholder': 'Apartment'
   }))


   zip_code = forms.CharField(widget=forms.TextInput(attrs={
       'class': 'form-control',
       'id': 'floatingZip',
       'placeholder': 'Zip code'
   }))
class CouponForm(forms.Form):
   code = forms.CharField(widget=forms.TextInput(attrs={
       'class': 'form-control',
       'placeholder': 'Coupon code'
   }))
