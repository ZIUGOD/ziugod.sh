from django.conf import settings  # type: ignore
from django.shortcuts import redirect, render, get_object_or_404  # type: ignore
from django.contrib.auth.decorators import login_required, login_not_required  # type: ignore
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.http import Http404, HttpResponse  # type: ignore
from features.notes.forms import NoteForm  # type: ignore
from .models import Note


@login_not_required
def index(request):
    if request.method == "GET":
        context = {
            "notes": Note.objects.all(),
        }
        return render(request, "index.html", context)

    else:
        return HttpResponse("Method not allowed", status=405)


@login_required
def create_note(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN}?next={request.path}")
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save()
        else:
            return render(request, "create_note.html", {"form": form})

        return redirect("index")

    else:
        form = NoteForm()
        return render(request, "create_note.html", {"form": form})


@login_not_required
def read_note(request, note_id):
    try:
        if request.method == "GET":
            context = {
                "note": get_object_or_404(Note, pk=note_id),
            }

        else:
            return HttpResponse("Method not allowed", status=405)

    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    return render(request, "read_note.html", context)


@login_required
def update_note(request, note_id):
    try:
        note = get_object_or_404(Note, pk=note_id)

        if request.method == "POST":
            note.title = request.POST.get("title")
            note.content = request.POST.get("content")
            note.save()

            return redirect("read_note", note_id=note.id)
        else:
            form = NoteForm(instance=note)

        return render(request, "update_note.html", {"form": form, "note": note})

    except Note.DoesNotExist:
        raise Http404("Note does not exist")


@login_required
def delete_note(request, note_id):
    try:
        note = get_object_or_404(Note, pk=note_id)

        if request.method == "POST":
            note.delete()

            return redirect("index")
        else:
            return render(request, "delete_note.html", {"note": note})

    except Note.DoesNotExist:
        raise Http404("Note does not exist")


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.post["password"],
        )

        if user:
            login(request, user)

        return redirect("index")

    return render(request, "index.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("index")
