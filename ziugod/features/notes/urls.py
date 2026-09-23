from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_note, name="create_note"),
    path("note/<int:note_pk>/", views.read_note, name="read_note"),
    path("update/<int:note_pk>/", views.update_note, name="update_note"),
    path("delete/<int:note_pk>/", views.delete_note, name="delete_note"),
]
