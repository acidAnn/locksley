"""Module for specifying basic settings for the application, including its name.

Classes:
AnnotationConfig
"""

from django.apps import AppConfig


class AnnotationConfig(AppConfig):
    """Configuration for the annotation app, the web interface part of Locksley."""
    name = "annotation"
