from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import LabelForm
from .models import Sentence, Batch


# Create your views here.
@login_required
def workbench(request):
    all_batches = Batch.objects.filter(assignee=request.user)
    return render(request, "annotation/workbench.jinja2", {"batches": all_batches, "message": "Willkommen in der Werkbank"})


@login_required
def sentence_view(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    sentence = batch.sentences.all()[0]
    if request.method == "GET":
        form = LabelForm(sentence=sentence)

    elif request.method == 'POST':
        form = LabelForm(request.POST)

        if form.is_valid():
            try:
                label = form.save(commit=False)
                label.user = request.user
                label.sentence = sentence
                label.save()
                return redirect("workbench")

            except IntegrityError as ie:
                return render(request, "annotation/sentence_view.jinja2", {"error": "Shit happens.", "sentence": sentence, "form": form})

    else:
        form = LabelForm(sentence=sentence)

    return render(request, "annotation/sentence_view.jinja2", {"sentence": sentence, "form": form})
