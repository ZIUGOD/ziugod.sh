from django import forms  # type: ignore[import]
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control bg-black border-secondary text-light font-monospace rounded-3",
                    "autocomplete": "off",
                    "autofocus": True,
                    "placeholder": "Title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control bg-black border-secondary text-light font-monospace rounded-3",
                    "rows": 14,
                    "placeholder": "Content",
                }
            ),
        }
