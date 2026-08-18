from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Note


class NoteModelTests(TestCase):
    def test_was_published_recently_with_future_note(self):
        """
        was_published_recently() returns False for Notes whose `created_at`
        is in the future.
        """
        time = timezone.now() + timedelta(days=30)
        future_note = Note(created_at=time)
        self.assertIs(future_note.was_published_recently(), False)

    def test_note_summary_truncates_long_content(self):
        note = Note(title="Long title", content="a" * 120)

        self.assertEqual(note.note_summary(), "a" * 100 + "...")


class NoteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret123",
        )

    def test_index_lists_existing_notes(self):
        note = Note.objects.create(title="First note", content="Hello from tests")

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")
        self.assertIn(note, response.context["notes"])

    def test_create_note_creates_and_redirects_to_index(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("create_note"),
            {"title": "New note", "content": "Created through tests"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(Note.objects.filter(title="New note").exists())

    def test_read_note_shows_existing_note(self):
        note = Note.objects.create(title="Read me", content="Body content")

        response = self.client.get(reverse("read_note", args=[note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Read me")
        self.assertContains(response, "Body content")

    def test_update_note_changes_content(self):
        self.client.force_login(self.user)
        note = Note.objects.create(title="Old title", content="Old content")

        response = self.client.post(
            reverse("update_note", args=[note.id]),
            {"title": "Updated title", "content": "Updated content"},
        )

        self.assertEqual(response.status_code, 302)
        note.refresh_from_db()
        self.assertEqual(note.title, "Updated title")
        self.assertEqual(note.content, "Updated content")

    def test_delete_note_removes_note(self):
        self.client.force_login(self.user)
        note = Note.objects.create(title="Delete me", content="Will be removed")

        response = self.client.post(reverse("delete_note", args=[note.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())
