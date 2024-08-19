from django.urls import re_path
from .views import main, poll, rpc

urlpatterns = [
    re_path("gyatt", rpc),
    re_path("poll/.+", poll),
    re_path('.*', main)
]