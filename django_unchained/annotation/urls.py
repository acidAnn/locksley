from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.workbench, name="workbench"),
    path("accounts", include('django.contrib.auth.urls')),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path("sentence-view/<int:batch_id>/", views.sentence_view, name="sentence-view"),
    path("testrun-view/<int:testrun_id>#<int:iterator>/", views.testrun_view, name="testrun-view"),
    path("completed/<int:batch_id>", views.completed, name="completed"),
    path("testrun-completed/", views.testrun_completed, name="testrun-completed"),
    path("instructions/", views.instructions, name="instructions"),
    path(
        "corpus-instructions/<int:corpus_id>/",
        views.corpus_instructions,
        name="corpus-instructions",
    ),
]
