"""Contain urls."""
from pathlib import Path
from django.urls import re_path, path
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import RPCHandler, BasicView

app_name = 'polls'

urlpatterns = static(
    "/assets/",
    document_root=Path(__file__).parents[1].joinpath(
        "frontend", "dist", "assets")) + [
            path("gyatt", RPCHandler.as_view(), name="gyatt"),
            path("polls", BasicView.as_view(), name="polls"),
            path("auth", BasicView.as_view(), name="auth"),
            path("login", lambda r: redirect("polls:auth")),
            re_path("create/.*", BasicView.as_view(), name="create"),
            re_path("poll/.+", BasicView.as_view(), name="poll"),
            re_path("res/.+", BasicView.as_view(), name="res"),
            path("", lambda r: redirect("polls:polls"))
        ]
