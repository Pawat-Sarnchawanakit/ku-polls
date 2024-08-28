"""Contain views."""
# pylint: disable=broad-exception-caught
from datetime import timedelta, datetime
from pathlib import Path
from json import loads, dumps
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, FileResponse
from django.db.models import Count
from django.utils import timezone
from django.views import View
from django.db.models import Q
from .models import Poll, Response, Session, User, get_or_none

FRONTEND = Path(__file__).parents[1].joinpath("frontend", "dist")


def check_auth(request: HttpRequest) -> User | None:
    """Check whether the user is authenticated.

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
    except Exception:
        return None


class RPCHandler(View):
    """Handle RPC requests."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle RPC requests."""
        json_data = loads(request.body)
        method = json_data.get("f")
        if not isinstance(method, str):
            return HttpResponse("Function name is missing or incorrect",
                                status=400)
        method = f"fn_{method}"
        if not hasattr(self, method):
            return HttpResponse("Function not found", status=404)
        del json_data["f"]
        return getattr(self, method)(request, **json_data)

    def fn_login(self, _: HttpRequest, u: str, p: str) -> HttpResponse:
        """Log the user in."""
        if not isinstance(u, str):
            return HttpResponse("Username must be a string", status=400)
        if not isinstance(p, str):
            return HttpResponse("Password must be a string", status=400)
        user = get_or_none(User, username=u)
        if user is None or not user.check_password(p):
            return HttpResponse("Invalid credentials.", status=400)
        session = user.create_session()
        response = HttpResponse("ok")
        response.set_cookie("tk", session.hex())
        return response

    def fn_regis(self, _: HttpRequest, u: str, p: str) -> HttpResponse:
        """Register the user."""
        if not isinstance(u, str):
            return HttpResponse("Username must be a string", status=400)
        if not isinstance(p, str):
            return HttpResponse("Password must be a string", status=400)
        user = get_or_none(User, username=u)
        if user is not None:
            return HttpResponse("User already exists.", status=400)
        user: User = User.register(username=u, password=p)
        session = user.create_session()
        response = HttpResponse("ok")
        response.set_cookie("tk", session.hex())
        return response

    def fn_create(self,
                  request: HttpRequest,
                  y: str,
                  b: int = None,
                  e: str = None,
                  n: str = "Unnamed poll",
                  i: str = '',
                  a: int = 0,
                  r: int = 0) -> HttpResponse:
        """Create a poll."""
        user = check_auth(request)
        if user is None:
            return HttpResponse("Unauthorized", status=401)
        if not isinstance(y, str):
            return HttpResponse("YAML must be a string.", status=400)
        if not isinstance(n, str):
            return HttpResponse("Name must be a string.", status=400)
        if not isinstance(r, int):
            return HttpResponse("Res must be an int.", status=400)
        if not isinstance(i, str):
            return HttpResponse("Image must be a string.", status=400)
        if not isinstance(a, int):
            return HttpResponse("Allow must be an int.", status=400)
        if b is None:
            b = timezone.now()
        elif not isinstance(b, int):
            return HttpResponse("Begin must be an int.", status=400)
        else:
            b = datetime.utcfromtimestamp(b)
        if e:
            cur_poll = get_or_none(Poll, id=e)
            if cur_poll is None:
                return HttpResponse("Not found", status=404)
            if cur_poll.creator != user:
                return HttpResponse("Forbidden", status=403)
            cur_poll.yaml = y
            cur_poll.name = n or 'Unnamed Poll'
            cur_poll.res = r
            cur_poll.image = i
            cur_poll.allow = a
            cur_poll.pub_date = b
            cur_poll.save()
            return HttpResponse(cur_poll.id)
        cur_poll = Poll.objects.create(yaml=y,
                                       name=n,
                                       res=r,
                                       image=i,
                                       creator=user,
                                       pub_date=b,
                                       allow=a)
        return HttpResponse(cur_poll.id)

    def fn_list(self, _: HttpRequest) -> HttpResponse:
        """List active polls."""
        now = timezone.now()
        polls = list(Poll.objects.filter(Q(pub_date__lte=now) & (Q(end_date__isnull=True) | Q(end_date__gt=now)), ) \
            .order_by("-pub_date")[:100].values(
            "id", "name", "image"))
        return HttpResponse(dumps(polls))

    def fn_res(self, request: HttpRequest, n: str) -> HttpResponse:
        """Return the responses and it's count."""
        if not isinstance(n, str):
            return HttpResponse("Poll number must be a string.", status=400)
        user = check_auth(request)
        poll = get_or_none(Poll, id=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        if not poll.can_view_responses(user):
            return HttpResponse("Forbidden", status=403)
        responses_list = Response.objects.filter(question=poll) \
            .values("key", "value") \
            .annotate(count=Count("value"))
        responses_dict = dict()
        for v in responses_list:
            val = responses_dict.get(v["key"])
            if val is None:
                val = []
                responses_dict[v["key"]] = val
            val.append({"value": v["value"], "count": v["count"]})
        return HttpResponse(dumps(responses_dict))

    def fn_aa(self, request: HttpRequest, n: str):
        """Check whether the poll is already answered."""
        poll = get_or_none(Poll, id=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        user = check_auth(request)
        if user is not None:
            if Response.objects.filter(submitter=user,
                                       question=poll).first() is not None:
                return HttpResponse("y")
            return HttpResponse("n")
        return HttpResponse("idk", status=401)

    def fn_submit(self, request: HttpRequest, n: str, r: dict = None):
        """Submit answers to database."""
        user = check_auth(request)
        poll = get_or_none(Poll, id=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        if not poll.can_vote(user):
            return HttpResponse("Forbidden", status=403)
        if user is not None:
            Response.objects.filter(submitter=user).delete()
        ress = []
        for k, v in (r or {}).items():
            ress.append(Response(question=poll, key=k, value=v,
                                 submitter=user))
        Response.objects.bulk_create(ress)
        return HttpResponse("ok")

    def fn_get(self, request: HttpRequest, n: str):
        """Get a poll."""
        user = check_auth(request)
        poll = Poll.objects.get(id=n)
        if not poll.can_view(user):
            return HttpResponse("Forbidden", status=403)
        return HttpResponse(
            dumps({
                "is_creator": user is not None and poll.creator == user,
                "login": user is None and poll.requires_auth(),
                "yaml": poll.yaml,
            }))


class BasicView(View):
    """Contain basic views like auth, polls, create, and responses."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Accept GET request for basic views."""
        name = request.resolver_match.url_name
        method = f"view_{name}"
        if hasattr(self, method):
            return getattr(self, method)(request)
        return HttpResponse("Page not found.", status=404)

    def view_auth(self, request: HttpRequest) -> HttpResponse:
        """Display login/register view."""
        if check_auth(request) is not None:
            return redirect("polls:polls")
        return FileResponse(open(FRONTEND.joinpath("auth", "index.html"),
                                 "rb"))

    def view_polls(self, _: HttpRequest) -> HttpResponse:
        """Display a list of polls."""
        return FileResponse(open(FRONTEND.joinpath("index.html"), "rb"))

    def view_create(self, request: HttpRequest) -> HttpResponse:
        """Display the poll creator view."""
        user = check_auth(request)
        if user is None:
            return redirect("polls:auth")
        return FileResponse(
            open(FRONTEND.joinpath("create", "index.html"), "rb"))

    def view_poll(self, _: HttpRequest) -> HttpResponse:
        """Return the html file for viewing the poll."""
        return FileResponse(open(FRONTEND.joinpath("poll", "index.html"),
                                 "rb"))

    def view_res(self, _: HttpRequest) -> HttpResponse:
        """Return the html file for results."""
        return FileResponse(open(FRONTEND.joinpath("res", "index.html"), "rb"))
