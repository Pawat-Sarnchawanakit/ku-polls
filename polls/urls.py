from django.urls import re_path, path
from .views import main, poll, rpc, create, auth, res
from django.conf.urls.static import static
from pathlib import Path

urlpatterns = static("/assets/", document_root=Path(__file__).parents[1].joinpath("frontend", "dist", "assets")) + [
    path("auth/", auth),
    path("create/", create),
    path("gyatt", rpc),
    re_path("poll/.+", poll),
    re_path("res/.+", res),
    path("", main)
]