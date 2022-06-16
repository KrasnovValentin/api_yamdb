from django import forms
from reviews.models import Genre


class TitleChangeListForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),
                                           required=False)
