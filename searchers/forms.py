from django import forms
from .models import Terms, CategoryModel

class TermsForm(forms.ModelForm):
    #new_synonyms = forms.CharField(required=False, help_text="Geben Sie Synonyme getrennt durch Kommas ein")

    class Meta:
        model = Terms
        fields = ['word']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['term_category', 'term_category_description']