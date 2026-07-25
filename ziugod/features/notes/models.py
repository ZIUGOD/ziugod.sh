from django.db import models

class Note(models.Model):
    """
    This is the single, definitive source of information about the data. It contains the essential fields and behaviors of the data are stored
    """
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text="Note title (Max. length: 100)",
    )
    content = models.TextField(
        help_text="The content of the note. No max. length",
    )
    created_at = models.DateField(
        auto_now_add=True,
        help_text="The moment the note was created.",
    )
    updated_at = models.DateField(
        auto_now=True,
        help_text="The moment of the last updated.",
    )
