from django.conf import settings  # type: ignore
from django.shortcuts import redirect, render, get_object_or_404  # type: ignore
from django.contrib.auth.decorators import login_required, login_not_required  # type: ignore
from django.template import context
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.http import Http404, HttpResponse, request  # type: ignore
from django.views.decorators.http import require_safe
from features.notes.forms import NoteForm  # type: ignore
from .models import Note


@require_safe  # Allows only GET and HEAD requests, returning a 405 Method Not Allowed response for other methods
@login_not_required
def index(request):
    context = {
        "notes": Note.objects.order_by("-created_at"),
    }
    return render(request, "index.html", context)


@login_required
def create_note(request):
    if request.method == "POST":  # POSTing a new note
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()

            return redirect("index")

    elif request.method == "GET":  # rendering the form to create a new note
        form = NoteForm()

        return render(request, "create_note.html", {"form": form})

    else:  # request method is neither GET nor POST
        return HttpResponse("Method not allowed", status=405)


@login_not_required
def read_note(request, note_pk):
    if request.method == "GET":
        note = get_object_or_404(Note, pk=note_pk)  # the note itself

        context = {"note": note}
        context["is_author"] = request.user == note.author

        return render(request, "read_note.html", context)

    else:
        return HttpResponse("Method not allowed", status=405)


@login_required
def update_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk, author=request.user)  # the note itself

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note = form.save()

            return redirect("read_note", note_pk=note.id)

        else:
            return render(request, "update_note.html", {"form": form, "note": note})

    elif request.method == "GET":
        form = NoteForm(instance=note)
        context = {"form": form, "note": note}

        return render(request, "update_note.html", context)

    else:
        return HttpResponse("Method not allowed", status=405)


@login_required
def delete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if request.method == "POST":

        if request.user == note.author:
            note.delete()  # deleting the note for real

            return redirect("index")

        else:
            return HttpResponse(
                "You are not authorized to delete this note.", status=403
            )

    else:
        return render(request, "delete_note.html", {"note": note})
