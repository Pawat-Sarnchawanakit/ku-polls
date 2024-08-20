from django.urls import re_path
from .views import main, poll, rpc, create

urlpatterns = [
    re_path("create/", create),
    re_path("gyatt", rpc),
    re_path("poll/.+", poll),
    re_path('.*', main)
]