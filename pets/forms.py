from django import forms

from .models import ReviewWorkers


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = ReviewWorkers
        fields = ("name", "email", "text")
