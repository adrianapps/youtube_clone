from django import forms
from .models import Comment, Video, Channel


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

    def __init__(self, user, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(user=user)

