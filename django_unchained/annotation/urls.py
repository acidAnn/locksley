from django.urls import path
from . import views

urlpatterns = [
    path('', views.workbench, name='workbench'),
    path('sentence-view/<int:batch_id>/', views.sentence_view, name='sentence-view'),
]
