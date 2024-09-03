"""Contain urls."""
from pathlib import Path
from django.urls import path
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import RPCHandler, BasicView, RegisterView

app_name = 'polls'

urlpatterns = [
        path("gyatt", RPCHandler.as_view(), name="gyatt"),
        path("polls", BasicView.as_view(), name="polls"),
        path("auth", lambda r: redirect("login")),
        path("login", lambda r: redirect("login")),
        path("admin", lambda r: redirect("polls:create")),
        path("create/", BasicView.as_view(), name="create"),
        path("register", RegisterView.as_view(), name="register"),
        path("create/<int:poll_id>", BasicView.as_view(), name="create"),
        path("poll/<int:poll_id>", BasicView.as_view(), name="poll"),
        path("polls/<int:poll_id>",
             lambda r, poll_id=None: redirect("polls:poll", poll_id=poll_id)),
        path("res/<int:poll_id>", BasicView.as_view(), name="res"),
        path("", lambda r: redirect("polls:polls"))
    ] + static(
    "/",
    document_root=Path(__file__).parents[1].
    joinpath("frontend", "dist"))
