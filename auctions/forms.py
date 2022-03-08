from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}) ,max_length=64)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}) ,max_length=256)
    CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('HOME', 'Home'),
        ('FASHION', 'Fashion'),
        ('OTHER', 'Other'),
    ]
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=CHOICES)
    starting_bid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Starting bid: (USD)'}))
    image = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Please place the image URL here!'}))

class NewBidForm(forms.Form):
    bid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Place Bid'}), label="")