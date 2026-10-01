document.addEventListener("DOMContentLoaded", () => {
    const buttonDeleteNote = document.getElementById("confirm-delete");

    if (!buttonDeleteNote) { return };

    buttonDeleteNote.disabled = true;

    setTimeout(() => {
        buttonDeleteNote.disabled = false;
    }, 1750);
});
