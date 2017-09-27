from django import forms


class ValidatorForm(forms.Form):
    number = forms.CharField(label='Credit Card Number',
                             required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Credit Card Number'}))
    file = forms.FileField(required=False,
                           widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                  'class': 'form-control',
                                                                  'placeholder': 'Upload file'}))
