from django import forms

from .models import Post, Comment
from froala_editor.widgets import FroalaEditor


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "image", "thumbnail"]
        widgets = {
            'content': FroalaEditor(),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'placeholder':'Write a comment...'}), label='')

    class Meta:
        model = Comment
        fields = ['content']