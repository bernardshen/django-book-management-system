from django import forms

class ReaderForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    age = forms.IntegerField()