from django import forms

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}), max_length=100)
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Enter Markdown'}))

class EditEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Enter Markdown'}))
    
