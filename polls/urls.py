from pathlib import Path
from django.urls import re_path, path
from django.conf.urls.static import static
from .views import main, poll, rpc, create, auth, res

urlpatterns = static("/assets/", document_root=Path(__file__).parents[1].joinpath("frontend", "dist", "assets")) + [
    path("polls", main),
    path("polls/", main),
    path("auth/", auth),
    path("login", auth),
    re_path("create/.*", create),
    path("gyatt", rpc),
    re_path("poll/.+", poll),
    re_path("res/.+", res),
    path("", main)
]