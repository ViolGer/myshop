from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'details']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your experience...'}),
        }
    def clean_comment(self):
        text = (self.cleaned_data.get('comment') or '').strip()
        if not text:
            raise forms.ValidationError('Write a few words..')
        return text