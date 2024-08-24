import secrets
import hmac
import enum
from datetime import timedelta, datetime
from pathlib import Path
from json import loads, dumps
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, FileResponse
from django.db.models import Count
from django.utils import timezone
from .models import Poll, Response, Session, User

FRONTEND = Path(__file__).parents[1].joinpath("frontend", "dist")


class AuthType(enum.Enum):
    Client = 1
    Auth = 1 << 1


class ResType(enum.Enum):
    Creator = 1
    Auth = 1 << 1


def create(request: HttpRequest):
    user = check_auth(request)
    if user is None:
        return redirect("/auth/")
    return FileResponse(open(FRONTEND.joinpath("create", "index.html"), "rb"))


def check_auth(request: HttpRequest) -> User | None:
    """Checks whether the user is authenticated.

    Args:
        request (HttpRequest): The request to check.

    Returns:
        User | None: The user if authenticated or None.
    """
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
        return None


def create_session(user: User) -> str:
    """Creates a session for a user

    Args:
        user (User): The user to create a session for

    Returns:
        string: The session key created.
    """
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
    """Returns the login/register page."""
    if check_auth(request) is not None:
        return redirect("/")
    return FileResponse(open(FRONTEND.joinpath("auth", "index.html"), "rb"))


def main(request: HttpRequest):
    """Returns home page otherwise display 404 error."""
    if len(request.path) <= 1:
        return FileResponse(open(FRONTEND.joinpath("index.html"), "rb"))
    return HttpResponse(
        "<h1 style=\"text-align: center; margin: auto\">404</h1>"
        "<p style=\"text-align: center\">Dumb bitch, go back to your pen.</p>"
    )


def rpc(request: HttpRequest):
    """Handles RPC requests"""
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
        if data.get("y") is None:
            return HttpResponse("bad", status=400)
        try:
            poll = None
            edit = data.get('e')
            if edit:
                poll = Poll.objects.get(id=edit)
                if poll is None:
                    return HttpResponse("Not found", status=404)
                if poll.creator != user:
                    return HttpResponse("Forbidden", status=403)
                poll.yaml = data["y"]
                poll.name = data.get("n", 'Unnamed Poll')
                poll.image = data.get("i", '')
                poll.allow = int(data.get("a", 0))
            else:
                date = data.get('b')
                print(date)
                if date is None:
                    date = timezone.now()
                else:
                    date = datetime.utcfromtimestamp(date)
                poll = Poll(yaml=data.get("y", ''),
                            name=data.get("n", 'Unnamed Poll'),
                            res=data.get("r"),
                            image=data.get("i", ''),
                            creator=user,
                            pub_date=date,
                            allow=int(data.get("a", 0)))
            poll.save()
        except Exception as e:
            return HttpResponse(str(e), status=500)
        return HttpResponse(poll.id)
    if func == "list":
        try:
            polls = Poll.objects.filter(pub_date__lte=timezone.now()) \
                .order_by("-pub_date")[:100].values(
                "id", "name", "image")
            return HttpResponse(dumps(list(polls)))
        except Exception as e:
            return HttpResponse(str(e), status=500)
    if func == "res":
        try:
            user = check_auth(request)
            poll = Poll.objects.get(id=data.get("n"))
            if not (((poll.res & ResType.Creator.value) != 0) and \
                user is not None and poll.creator == user or \
                poll.res == 0 or \
                ((poll.res & ResType.Auth.value) != 0) and user is not None):
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
            if poll.pub_date > timezone.now():
                return HttpResponse("Forbidden", status=403)
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
            user = check_auth(request)
            poll = Poll.objects.get(id=data.get("n"))
            is_creator = user is not None and poll.creator == user
            if poll.pub_date > timezone.now() and not is_creator:
                return HttpResponse("Forbidden", status=403)
            return HttpResponse(
                dumps({
                    "is_creator":
                    is_creator,
                    "login":
                    user is None
                    and (poll.allow != 0 and
                         (poll.allow & AuthType.Client.value) == 0),
                    "yaml":
                    poll.yaml,
                }))
        except Exception as e:
            return HttpResponse(str(e), status=500)
    return HttpResponse("bad", status=400)


def poll(_: HttpRequest):
    """Returns the html file for viewing the poll."""
    return FileResponse(open(FRONTEND.joinpath("poll", "index.html"), "rb"))


def res(_: HttpRequest):
    """Returns the html file for results."""
    return FileResponse(open(FRONTEND.joinpath("res", "index.html"), "rb"))
