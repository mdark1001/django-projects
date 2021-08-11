"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 11/08/21
@name: forms
"""
from django import forms


class EmailForm(forms.Form):
    """  Enviar correos desde un formulario en django """
    name = forms.CharField(
        max_length=25,
    )
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
