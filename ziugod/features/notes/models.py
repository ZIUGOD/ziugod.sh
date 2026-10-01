import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Note(models.Model):
    title = models.CharField(
        max_length=128,
        unique=True,
        help_text="Note title (Max. length: 128)",
    )

    content = models.TextField(
        help_text="The content of the note. No max. length",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The moment the note was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The moment of the last update.",
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notes",
    )

    # Representation methods

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        for word in self.content.split():
            yield word

    # Note analysis methods

    def age(self):
        delta = timezone.now().replace(microsecond=0) - self.created_at.replace(
            microsecond=0
        )

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}h {minutes:02}m {seconds:02}s"

    def note_summary(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=3) <= self.created_at <= now

    # URL methods

    def get_absolute_url(self):
        return reverse("read_note", args=[str(self.id)])

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        db_table = "notes"

    @classmethod
    def create(cls, title, content, author):
        note = cls(
            title=title,
            content=content,
            author=author,
        )
        note.save()

        return note
