from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import LabelFormSet, SignUpForm, TestRunLabelFormSet
from .models import Sentence, Batch, Membership, Corpus, RelationType, TestRun, ExampleSentence, GoldLabel


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account für {username} erfolgreich angelegt!')
            return redirect("workbench")

    else:
        form = SignUpForm()

    return render(request, "registration/signup.jinja2", {"form": form})


@login_required
def profile(request):
    return render(request, "annotation/profile.jinja2")


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
            "testruns": TestRun.objects.all(),
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
def testrun_completed(request):
    return render(
        request,
        "annotation/testrun_completed.jinja2",
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
                        print("is valid")

                        try:
                            label = form.save(commit=False)
                            label.user = request.user
                            label.sentence = sentence
                            label.save()

                        except IntegrityError:
                            print("integrity error")

                        finally:
                            membership = Membership.objects.get(sentence=sentence, batch=batch)
                            membership.labeled = True
                            membership.save()

                    else:
                        print("INVALID FORM")

                batch.number_of_labeled_sentences += 1
                batch.save()

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
                "batch": batch,
                "entities": sentence.entity_set.all(),
                "relation_types": RelationType.objects.filter(corpus=sentence.corpus),
                "formset": formset},
        )


@login_required
def testrun_view(request, testrun_id, iterator):
    testrun = TestRun.objects.get(id=testrun_id)

    if iterator >= testrun.examplesentence_set.count():
        return redirect("testrun-completed")

    else:
        example_sentence = ExampleSentence.objects.filter(testrun=testrun_id)[iterator]
        goldlabels = GoldLabel.objects.filter(example_sentence=example_sentence)

        iterator += 1

        if request.method == "POST":
                return redirect("testrun-view", testrun_id=testrun_id, iterator=iterator)
        else:
            formset = TestRunLabelFormSet(form_kwargs={"example_sentence": example_sentence})

        return render(
            request,
            "annotation/testrun_view.jinja2",
            {
                "sentence": example_sentence,
                "testrun": testrun,
                "entities": example_sentence.exampleentity_set.all(),
                "formset": formset,
                "iterator": iterator,
                "testrun_size": testrun.examplesentence_set.count(),
                "goldlabels": goldlabels
            },
        )

