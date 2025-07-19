from django import forms
from django.forms import Textarea
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={"rows": 2}),
        }
