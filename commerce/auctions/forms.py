from django import forms

from auctions.models import Comment, Auction

class NewAuctionForm(forms.ModelForm):
    title = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter a title', 'style': 'width:400px; margin-bottom:20px; margin-left:20px', 'class': 'form-control'}))
    description = forms.CharField(label="", max_length=250, widget=forms.Textarea(attrs={'placeholder': 'Enter a description', 'style': 'height:100px; width:400px; margin-left:20px;', 'class': 'form-control'}))
    bid = forms.DecimalField(label="", max_digits=8, decimal_places=2, max_value=99999999, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Initial bid', 'class': 'form-control', 'step': '1', 'style': 'height:50px; width:400px; margin:20px;', 'class': 'form-control'}))
    picture_url = forms.CharField(label="", max_length=200,widget=forms.Textarea(attrs={'placeholder': 'Enter a picture url', 'style': 'height:50px; width:400px; margin-left:20px;', 'class': 'form-control'}))
    category = forms.ChoiceField(label="", widget=forms.Select(attrs={'style': 'height:50px; width:150px; margin:20px; margin-bottom:0px;', 'class': 'form-control'}), choices=Auction.Categories.choices)

    class Meta:
        model = Auction
        exclude = ("author", "buyer", "created_date", "status")

class NewBidForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    bid = forms.DecimalField(label="", max_digits=8, decimal_places=2, max_value=99999999, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Your bid', 'style': 'height:50px; width:400px;', 'class': 'form-control'}))
    
    class Meta:
        model = Auction
        fields = ('bid', 'id')

class NewCommentForm(forms.ModelForm):
    comment = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your comment', 'style': 'width:400px; margin-bottom:15px;', 'class': 'form-control'}))
    
    class Meta:
        model = Comment
        fields = ('comment',)