from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import LabelForm, LabelFormSet
from .models import Sentence, Batch, Membership, Corpus, RelationType


@login_required
def workbench(request):
    corpora = Corpus.objects.all()
    all_batches = Batch.objects.filter(assignee=request.user)
    return render(
        request,
        "annotation/workbench.jinja2",
        {
            "batches": all_batches,
            "corpora": corpora,
            "message": "Willkommen in der Werkbank",
        },
    )


@login_required
def instructions(request):
    return render(request, "annotation/instructions.jinja2", {"user": request.user})


@login_required
def corpus_instructions(request, corpus_id):
    corpus = Corpus.objects.get(id=corpus_id)
    relation_types = RelationType.objects.filter(corpus=corpus_id)
    return render(
        request,
        "annotation/corpus-instructions.jinja2",
        {"corpus": corpus, "relation_types": relation_types},
    )


@login_required
def completed(request, batch_id):
    return render(
        request,
        "annotation/completed.jinja2",
        {"batch_id": batch_id}
    )


@login_required
def sentence_view(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    unlabeled_members = Membership.objects.filter(batch=batch, labeled=False)

    if not unlabeled_members:
        return redirect("completed", batch_id=batch_id)

    else:
        first_unlabeled_member = unlabeled_members[0]
        sentence = Sentence.objects.get(id=first_unlabeled_member.sentence.id)

        if request.method == "POST":
            formset = LabelFormSet(request.POST)
            for form in formset:
                print(form)

            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        label = form.save(commit=False)
                        print(label.subject)
                        print(label.object)

                        if not label.subject and not label.object:
                            print("no label necessary")
                            continue

                        else:
                            label.user = request.user
                            label.sentence = sentence
                            label.save()

                            membership = Membership.objects.get(sentence=sentence, batch=batch)
                            membership.labeled = True
                            membership.save()

                            batch.number_of_labeled_sentences += 1
                            batch.percentage_labeled = (
                                batch.number_of_labeled_sentences * 100
                            ) / batch.number_of_sentences
                            batch.save()

                    else:
                        print("INVALID FORM")

                return redirect("sentence-view", batch_id=batch_id)
            else:
                print("INVALID FORM")

        else:
            formset = LabelFormSet(form_kwargs={"sentence": sentence})

        return render(
            request,
            "annotation/sentence_view.jinja2",
            {
                "sentence": sentence,
                "entities": sentence.entities.all(),
                "relation_types": RelationType.objects.filter(corpus=sentence.corpus),
                "formset": formset},
        )


@login_required
def home(request):
    batch = Batch.objects.get(id=4)
    unlabeled_members = Membership.objects.filter(batch=batch, labeled=False)

    if not unlabeled_members:
        # TODO: alert error - already done
        return redirect("workbench")

    else:
        first_unlabeled_member = unlabeled_members[0]
        sentence = Sentence.objects.get(id=first_unlabeled_member.sentence.id)

        if request.method == "POST":
            formset = LabelFormSet(request.POST)

            if formset.is_valid():
                try:
                    labels = formset.save(commit=False)

                    for label in labels:
                        label.user = request.user
                        label.sentence = sentence
                        label.save()

                    membership = Membership.objects.get(sentence=sentence, batch=batch)
                    membership.labeled = True
                    membership.save()

                    batch.number_of_labeled_sentences += 1
                    batch.percentage_labeled = (
                        batch.number_of_labeled_sentences * 100
                    ) / batch.number_of_sentences
                    batch.save()

                    return redirect("sentence-view", batch_id=4)

                except IntegrityError as ie:
                    print(ie)
                    return render(
                        request,
                        "annotation/home.jinja2",
                        {
                            "error": "Shit happens.",
                            "sentence": sentence,
                            "entities": sentence.entities.all(),
                            "relation_types": RelationType.objects.all(),
                            "formset": formset,
                        },
                    )

        else:
            formset = LabelFormSet(form_kwargs={"sentence": sentence})

        print(type(formset), len(formset))
        return render(
            request,
            "annotation/home.jinja2",
            {
                "sentence": sentence,
                "entities": sentence.entities.all(),
                "relation_types": RelationType.objects.all(),
                "formset": formset},
        )

