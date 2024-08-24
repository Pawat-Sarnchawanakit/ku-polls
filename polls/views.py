from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, FileResponse
from django.db.models import Count
from pathlib import Path, PurePath
from json import loads, dumps
from django.utils import timezone, timesince
from django.contrib.staticfiles.views import serve
from datetime import timedelta
import secrets
import hmac
import enum
from .models import Poll, Response, Session, User

FRONTEND = Path(__file__).parents[1].joinpath("frontend", "dist")


class AuthType(enum.Enum):
    Client = 1
    Auth = 1 << 1


def create(request: HttpRequest):
    user = check_auth(request)
    if user is None:
        return redirect("/auth/")
    return FileResponse(open(FRONTEND.joinpath("create", "index.html"), "rb"))


def check_auth(request: HttpRequest):
    try:
        session_id = request.COOKIES.get("tk")
        if session_id is None:
            return None
        session = Session.objects.get(session=bytes.fromhex(session_id))
        if session.accessed <= timezone.now() - timedelta(days=2):
            session.accessed = timezone.now()
            session.save()
        return session.user
    except Exception as e:
        print(str(e))
        return None


def create_session(user: User):
    # Remove sessions older than 30 days.
    Session.objects.filter(user=user,
                           accessed__lte=timezone.now() -
                           timedelta(days=30)).delete()
    # Create session
    session_key = secrets.token_bytes(64)
    session = Session(user=user, session=session_key)
    session.save()
    return session_key


def auth(request: HttpRequest):
    if check_auth(request) is not None:
        return redirect("/")
    return FileResponse(open(FRONTEND.joinpath("auth", "index.html"), "rb"))


def main(request: HttpRequest):
    if len(request.path) <= 1:
        return FileResponse(open(FRONTEND.joinpath("index.html"), "rb"))
    return HttpResponse(
        "<h1 style=\"text-align: center; margin: auto\">404</h1><p style=\"text-align: center\">Dumb bitch, go back to your pen.</p>"
    )


def rpc(request: HttpRequest):
    data = None
    try:
        data = loads(request.body)
    except:
        pass
    if data is None:
        return HttpResponse("bad", status=400)
    func = data.get("f")
    if func == "login":
        username = data.get("u", "")
        password = bytes(data.get("p", ""), 'utf-8')
        user: User | None = None
        try:
            user = User.objects.get(username=username)
        except:
            pass
        if user is None:
            return HttpResponse("Invalid credentials.", status=400)
        if not hmac.compare_digest(
                hmac.digest(user.password_salt, password, "blake2b"),
                user.password_hash):
            return HttpResponse("Invalid credentials.", status=400)
        try:
            user = User.objects.get(username=username)
            session = create_session(user)
            res = HttpResponse("ok")
            res.set_cookie("tk", session.hex())
            return res
        except:
            return HttpResponse("err", status=500)
    if func == "regis":
        username = data.get("u", "")
        password = bytes(data.get("p", ""), 'utf-8')
        user: User | None = None
        try:
            user = User.objects.get(username=username)
        except:
            pass
        if user is not None:
            return HttpResponse("User already exists.", status=400)
        salt = secrets.token_bytes(64)
        pw_hash = hmac.digest(salt, password, "blake2b")
        try:
            user = User(username=username,
                        password_hash=pw_hash,
                        password_salt=salt)
            user.save()
            session = create_session(user)
            res = HttpResponse("ok")
            res.set_cookie("tk", session.hex())
            return res
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "create":
        user = check_auth(request)
        if user is None:
            return HttpResponse("Unauthorized", status=401)
        if data.get("y") == None:
            return HttpResponse("bad", status=400)
        try:
            poll = Poll(yaml=data["y"],
                        name=data.get("n", 'Unnamed Poll'),
                        image=data.get("i", ''),
                        creator=user,
                        allow=int(data.get("a", 0)))
            poll.save()
        except Exception as e:
            return HttpResponse(str(e), status=500)
        return HttpResponse(poll.id)
    if func == "list":
        try:
            polls = Poll.objects.order_by("-pub_date")[:100].values(
                "id", "name", "image")
            return HttpResponse(dumps(list(polls)))
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "res":
        try:
            user = check_auth(request)
            if user is None:
                return HttpResponse("Unauthorized", status=401)
            poll = Poll.objects.get(id=data.get("n"))
            if poll.creator != user:
                return HttpResponse("Forbidden", status=403)
            ress = Response.objects.filter(question=poll) \
                .values("key", "value") \
                .annotate(count=Count("value"))
            out = dict()
            for v in ress:
                val = out.get(v["key"])
                if val is None:
                    val = []
                    out[v["key"]] = val
                val.append({"value": v["value"], "count": v["count"]})
            return HttpResponse(dumps(out))
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "aa":
        try:
            poll = Poll.objects.get(id=data.get("n"))
            if poll is None:
                return HttpResponse("?", status=404)
            user = check_auth(request)
            if user is not None:
                if Response.objects.filter(submitter=user,
                                           question=poll).first() is not None:
                    return HttpResponse("y")
                return HttpResponse("n")
            return HttpResponse("?", status=401)
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "submit":
        try:
            user = check_auth(request)
            poll = Poll.objects.get(id=data.get("n"))
            can_submit = poll.allow == 0 or (poll.allow
                                             & AuthType.Client.value) != 0
            if not can_submit:
                if (poll.allow & AuthType.Auth.value) != 0:
                    if user is not None:
                        Response.objects.filter(submitter=user,
                                                question=poll).delete()
                        can_submit = True
            if not can_submit:
                return HttpResponse("Forbidden", status=403)
            ress = []
            for k, v in (data.get("r", {})).items():
                ress.append(
                    Response(question=poll, key=k, value=v, submitter=user))
            Response.objects.bulk_create(ress)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "get":
        try:
            poll = Poll.objects.get(id=data.get("n"))
            return HttpResponse(poll.yaml)
        except Exception as e:
            return HttpResponse(str(e), status=500)
    return HttpResponse("bad", status=400)


def poll(request: HttpRequest):
    return FileResponse(open(FRONTEND.joinpath("poll", "index.html"), "rb"))


def res(request: HttpRequest):
    return FileResponse(open(FRONTEND.joinpath("res", "index.html"), "rb"))
