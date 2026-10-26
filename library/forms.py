from django import forms
from django.core.exceptions import ValidationError
from .models import Book
import datetime

class BookForm(forms.ModelForm):
    """
    Form for adding and editing library catalog books with validation.
    """
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'category',
            'publication_year',
            'available_copies'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title (e.g. Higher Engineering Mathematics)'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name(s) (e.g. Dr. B. S. Grewal)'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10 or 13 digit ISBN (e.g. 978-8174091955)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1500,
                'max': datetime.date.today().year + 1
            }),
            'available_copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '').strip()
        # Remove hyphens and spaces for basic format check
        clean_code = isbn.replace('-', '').replace(' ', '')
        if len(clean_code) not in (10, 13):
            raise ValidationError("ISBN must be either 10 or 13 digits (excluding hyphens).")
        
        # Check uniqueness excluding current instance
        qs = Book.objects.filter(isbn=isbn)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A book with this ISBN already exists in the catalog.")
        
        return isbn

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        current_year = datetime.date.today().year
        if year and (year < 1500 or year > current_year + 1):
            raise ValidationError(f"Publication year must be between 1500 and {current_year + 1}.")
        return year

    def clean_available_copies(self):
        copies = self.cleaned_data.get('available_copies')
        if copies is not None and copies < 0:
            raise ValidationError("Available copies cannot be negative.")
        return copies
