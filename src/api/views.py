from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, FileResponse
from django.db.models import Count
from pathlib import Path
from json import loads, dumps

from .models import Poll, Response

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
    func = data.get("f")
    if func == "create":
        if data.get("y") == None:
            return HttpResponse("bad")
        poll = Poll(yaml=data["y"], name=data.get("n"), image=data.get("i"))
        poll.save()
        return HttpResponse(poll.id)
    if func == "list":
        try:
            polls = Poll.objects.all().order_by("-pub_date")[:100].values("id", "name", "image")
            return HttpResponse(dumps(list(polls)))
        except Exception as e:
            return HttpResponse(str(e))
    if func == "res":
        try:
            poll = Poll.objects.get(id=data.get("n"))
            ress = Response.objects.all() \
                .filter(question=poll) \
                .values("key", "value") \
                .annotate(count=Count("value"))
            out = dict()
            for v in ress:
                val = out.get(v["key"])
                if val is None:
                    val = []
                    out[v["key"]] = val
                val.append({
                    "value": v["value"],
                    "count": v["count"]
                })
            return HttpResponse(dumps(out))
        except Exception as e:
            return HttpResponse(str(e))
    if func == "submit":
        try:
            poll = Poll.objects.get(id=data.get("n"))
            ress = []
            for k, v in (data.get("r", {})).items():
                ress.append(Response(question=poll, key=k, value=v))
            Response.objects.bulk_create(ress)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(str(e))
    if func == "get":
        try:
            poll = Poll.objects.get(id=data.get("n"))
            return HttpResponse(poll.yaml)
        except Exception as e:
            return HttpResponse(str(e))
    return HttpResponse("bad")
    

def poll(request: HttpRequest):
    path = Path(__file__).parents[1].joinpath("frontend", "dist", "index.html")
    file = open(path, "rb")
    return FileResponse(file)