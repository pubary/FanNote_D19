from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 120, 'rows': 1},),
        label='Заголовок'
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'photo', 'file']
        widgets = {
            'category': forms.RadioSelect(attrs={'class': 'input-group', }),
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 5}),
            'photo': forms.ClearableFileInput(),
            'file': forms.ClearableFileInput(),
        }
