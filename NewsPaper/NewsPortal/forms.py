from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    post_title = forms.CharField(max_length=20)

    class Meta:
        model = Post
        fields = [
            'who_author',
            'time_in',
            'category_post',
            'post_title',
            'post_text',
            'post_rating',
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        post_text = cleaned_data.get("post_text")

        if post_title == post_text:
            raise ValidationError(
                "Описание не должно быть идентично заголовку."
            )

        return cleaned_data
