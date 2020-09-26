from django import forms

from posts.models import Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'cover',
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if Post.objects.filter(title=data).exists():
            raise forms.ValidationError("Title should be unique")
        return data


class UpdatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'cover',
        ]