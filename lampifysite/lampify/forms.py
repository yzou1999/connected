from django import forms

class ContactForm(forms.Form):
    songs = forms.CharField(label="song you want to play")