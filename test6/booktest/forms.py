from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post


class PostForm(forms.Form):
    # ckeditor widget
    content = forms.CharField(widget=CKEditorWidget())

