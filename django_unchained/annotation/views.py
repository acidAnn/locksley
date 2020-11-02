"""Module for the views of the annotation interface.

Functions:
signup
profile
workbench
instructions
corpus_instructions
testrun_completed
completed
sentence_view
testrun_view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import LabelFormSet, SignUpForm, TestRunLabelFormSet
from .models import Sentence, Batch, Membership, Corpus, RelationType, TestRun, ExampleSentence, GoldLabel


def signup(request: HttpRequest) -> HttpResponse:
    """A view in which a user can sign up for the annotation platform.

    :param request: HttpRequest
    :return: a HttpResponse
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account für {username} erfolgreich angelegt!')
            return redirect("workbench")

    else:
        form = SignUpForm()

    return render(request, "registration/signup.jinja2", {"form": form})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """A view that shows the name of the user who is logged in and a link to change their password.

    :param request: HttpRequest
    :return: a HttpResponse
    """
    return render(request, "annotation/profile.jinja2")


@login_required
def workbench(request: HttpRequest) -> HttpResponse:
    """The central home view for the user who is logged in.
    It links to the instructions, the corpus instructions and the batches that have been assigned to the user.

    :param request: HttpRequest
    :return: a HttpResponse
    """
    corpora = Corpus.objects.all()
    # find all batches that have been assigned to the user that is currently logged in
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
def instructions(request: HttpRequest) -> HttpResponse:
    """A view for general annotation instructions.

    :param request: HttpRequest
    :return: a HttpResponse
    """
    return render(request, "annotation/instructions.jinja2", {"user": request.user})


@login_required
def corpus_instructions(request: HttpRequest, corpus_id: int) -> HttpResponse:
    """A view for annotation instructions that are specific to the corpus in question.

    :param request: HttpRequest
    :param corpus_id: int id of the Corpus object in question
    """
    corpus = Corpus.objects.get(id=corpus_id)
    # only show description of relations that are predefined for the corpus in question
    relation_types = RelationType.objects.filter(corpus=corpus_id)
    return render(
        request,
        "annotation/corpus_instructions.jinja2",
        {"corpus": corpus, "relation_types": relation_types},
    )


@login_required
def completed(request: HttpRequest, batch_id: int) -> HttpResponse:
    """A view that is shown after a user has completed an annotation batch.

    :param request: HttpRequest
    :param batch_id: int id of the Batch object in question
    :return: a HttpResponse
    """
    return render(
        request,
        "annotation/completed.jinja2",
        {"batch_id": batch_id}
    )


@login_required
def testrun_completed(request: HttpRequest) -> HttpResponse:
    """A view that is displayed after a user has completed a test run.

    :param request: HttpRequest
    :return: a HttpResponse
    """
    return render(
        request,
        "annotation/testrun_completed.jinja2",
    )


@login_required
def sentence_view(request: HttpRequest, batch_id: int) -> HttpResponse:
    """A view for annotating an individual sentence from a given batch.

    :param request: HttpRequest
    :param batch_id: int id of the Batch object in question
    :return: a HttpResponse
    """
    batch = Batch.objects.get(id=batch_id)
    # find all sentences in the batch that have not been labeled yet
    unlabeled_members = Membership.objects.filter(batch=batch, labeled=False)

    if not unlabeled_members:
        # if there are no unlabeled sentences left, redirect to completed view
        return redirect("completed", batch_id=batch_id)

    else:
        # otherwise display the first unlabeled sentence in the batch
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
                            # set labeled status of sentence that has just been annotated to True for the current batch
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
def testrun_view(request: HttpRequest, testrun_id: int, iterator: int) -> HttpResponse:
    """A view for annotating an example sentence from a test run.

    :param request: HttpRequest
    :param testrun_id: int id of the TestRun object in question
    :param iterator: int counter of the next sentence in the test run
    :return: a HttpResponse
    """
    testrun = TestRun.objects.get(id=testrun_id)

    # when the end of the test run is reached, redirect to the testrun_completed view
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
