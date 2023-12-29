from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter a title', 'style': 'width:400px; margin-bottom:20px; margin-left:20px', 'class': 'form-control'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Enter a description', 'style': 'height:200px; width:800px; margin-left:20px;', 'class': 'form-control'}))

class EditPageForm(forms.Form):
    data = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Enter a description', 'style': 'height:200px; width:800px; margin-left:20px;', 'class': 'form-control'}))
