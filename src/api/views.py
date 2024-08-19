from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, FileResponse
from pathlib import Path
from json import loads

from .models import Poll

def main(request: HttpRequest):
    try:
        path = Path(__file__).parents[1].joinpath("frontend", "dist")
        path = path.joinpath(path, "index.html") if len(request.path) <= 1 or request.path.endswith("create") else path.joinpath(request.path.lstrip("/\\"))
        file = open(path, "rb")
        return FileResponse(file)
    except:
        pass
    return HttpResponse("<h1 style=\"text-align: center; margin: auto\">404</h1><p style=\"text-align: center\">Dumb bitch, go back to your pen.</p>")

def rpc(request: HttpRequest):
    data = None
    try:
        data = loads(request.body)
    except:
        pass
    if data is None:
        return HttpResponse("bad")
    if data["f"] == "create":
        if data["y"] == None:
            return HttpResponse("bad")
        poll = Poll(yaml=data["y"])
        poll.save()
        return HttpResponse(poll.id)
    if data["f"] == "submit":
        return HttpResponse("ok")
    if data["f"] == "get":
        poll = Poll.objects.get(id=data["n"])
        if poll is None:
            return HttpResponse("Poll does not exist.")
        return HttpResponse(poll.yaml)
    return HttpResponse("bad")
    

def poll(request: HttpRequest):
    path = Path(__file__).parents[1].joinpath("frontend", "dist", "index.html")
    file = open(path, "rb")
    return FileResponse(file)