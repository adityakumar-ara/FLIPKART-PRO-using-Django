from django import forms

from .models import Review

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
        label='Full name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        label='Email',
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        label='Phone',
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shipping address'}),
        label='Shipping address',
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City',
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State / province'}),
        label='State / Province',
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'}),
        label='Postal code',
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        label='Country',
    )
    payment_method = forms.ChoiceField(
        choices=(
            ('cod', 'Cash on Delivery'),
            ('upi', 'UPI Payment'),
            ('card', 'Card / Netbanking'),
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Payment method',
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Order notes (optional)'}),
        label='Order notes',
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts on this product...'}),
        }
