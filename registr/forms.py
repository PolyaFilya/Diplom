from django import forms

class QRForm(forms.Form):
    file = forms.ImageField()


