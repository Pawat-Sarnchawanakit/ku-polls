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
            path("create/<int:poll_id>", BasicView.as_view(), name="create"),
            path("poll/<int:poll_id>", BasicView.as_view(), name="poll"),
            path("polls/<int:poll_id>", lambda r, poll_id=None: redirect("polls:poll", poll_id=poll_id)),
            path("res/<int:poll_id>", BasicView.as_view(), name="res"),
            path("", lambda r: redirect("polls:polls"))
        ]
