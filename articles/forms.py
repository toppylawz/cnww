from django import forms
from .models import Entry, Tag

class ArticleForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=["tag","title","image","slug", "body","authors", "draft", "publish",]
