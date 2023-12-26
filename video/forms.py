from django import forms
from .models import Comment, Video


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...'})
        }
        fields = ['content']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['channel', 'title', 'file', 'description', 'thumbnail', 'tag']


