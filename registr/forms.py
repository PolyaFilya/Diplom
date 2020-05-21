from django import forms

import qreader

class QRForm(forms.Form):
    file = forms.ImageField()


