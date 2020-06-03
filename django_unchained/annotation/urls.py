from django.urls import path
from . import views

urlpatterns = [
    path("", views.workbench, name="workbench"),
    path("sentence-view/<int:batch_id>/", views.sentence_view, name="sentence-view"),
    path("home/", views.home, name="home"),
    path("completed/<int:batch_id>", views.completed, name="completed"),
    path("instructions/", views.instructions, name="instructions"),
    path(
        "corpus-instructions/<int:corpus_id>/",
        views.corpus_instructions,
        name="corpus-instructions",
    ),
]
