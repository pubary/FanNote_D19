from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'text',]
        widgets = {
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'category': forms.RadioSelect(attrs={'class': 'input-group', }),
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 8}),
        }
