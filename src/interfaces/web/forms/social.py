from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Share your thoughts...",
            }
        ),
        label="",
    )
