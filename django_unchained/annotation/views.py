from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import LabelForm
from .models import Sentence, Batch, Membership


@login_required
def workbench(request):
    all_batches = Batch.objects.filter(assignee=request.user)
    return render(request, "annotation/workbench.jinja2", {"batches": all_batches, "message": "Willkommen in der Werkbank"})


@login_required
def sentence_view(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    unlabeled_members = Membership.objects.filter(batch=batch, labeled=False)

    if not unlabeled_members:
        # TODO: alert error - already done
        return redirect("workbench")

    else:
        first_unlabeled_member = unlabeled_members[0]
        sentence = Sentence.objects.get(id=first_unlabeled_member.sentence.id)

        if request.method == 'POST':
            form = LabelForm(request.POST)

            if form.is_valid():
                try:
                    label = form.save(commit=False)
                    label.user = request.user
                    label.sentence = sentence
                    label.save()

                    membership = Membership.objects.get(sentence=sentence, batch=batch)
                    membership.labeled = True
                    membership.save()

                    return redirect("sentence-view", batch_id=batch_id)

                except IntegrityError as ie:
                    print(ie)
                    return render(request, "annotation/sentence_view.jinja2", {"error": "Shit happens.", "sentence": sentence, "entities": sentence.entities, "form": form})

        else:
            form = LabelForm(sentence=sentence)

        return render(request, "annotation/sentence_view.jinja2", {"sentence": sentence, "form": form})
