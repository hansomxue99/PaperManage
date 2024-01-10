from django import forms
from .models import PaperInfo


class PaperInfoForm(forms.ModelForm):
    class Meta:
        model = PaperInfo
        fields = (
            'title',
            'author',
            'paper_author',
            'source',
            'body',
            'tags',
            'reference',
            'pdf_file'
        )
