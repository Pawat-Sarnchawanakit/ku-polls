"""Contain views."""
# pylint: disable=broad-exception-caught
from datetime import timedelta, datetime
from pathlib import Path
from json import loads, dumps
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, FileResponse
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.contrib import messages
from .models import Poll, Response, Session, User, get_or_none

FRONTEND = Path(__file__).parents[1].joinpath("frontend", "dist")


def check_auth(request: HttpRequest) -> User | None:
    """Check whether the user is authenticated.

    Args:
        request (HttpRequest): The request to check.

    Returns:
        User | None: The user if authenticated or None.
    """
    session_id = request.COOKIES.get("tk")
    if session_id is None:
        return None
    session = get_or_none(Session, session=bytes.fromhex(session_id))
    if session is None:
        return None
    if session.accessed <= timezone.now() - timedelta(days=2):
        session.accessed = timezone.now()
        session.save()
    return session.user


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
                  c: int = None,
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
        if c is None:
            pass
        elif not isinstance(c, int):
            return HttpResponse("End must be an int.", status=400)
        else:
            c = timezone.make_aware(datetime.utcfromtimestamp(c))
        if b is None:
            b = timezone.now()
        elif not isinstance(b, int):
            return HttpResponse("Begin must be an int.", status=400)
        else:
            b = timezone.make_aware(datetime.utcfromtimestamp(b))
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
                                       end_date=c,
                                       allow=a)
        return HttpResponse(cur_poll.id)

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
        return HttpResponse(dumps(poll.get_responses()))

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
        poll = get_or_none(Poll, id=n)
        if poll is None:
            return HttpResponse("Not found", status=404)
        return HttpResponse(
            dumps({
                "is_creator": user is not None and poll.creator == user,
                "can_vote": poll.can_vote(user),
                "can_res": poll.can_view_responses(user),
                "closed": poll.is_closed(),
                "yaml": poll.yaml if poll.can_view(user) else None,
            }))


class BasicView(View):
    """Contain basic views like auth, polls, create, and responses."""

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        """Accept GET request for basic views."""
        name = request.resolver_match.url_name
        method = f"view_{name}"
        if hasattr(self, method):
            return getattr(self, method)(request, **kwargs)
        return HttpResponse("Page not found.", status=404)

    def view_auth(self, request: HttpRequest) -> HttpResponse:
        """Display login/register view."""
        if check_auth(request) is not None:
            return redirect("polls:polls")
        return FileResponse(open(FRONTEND.joinpath("auth", "index.html"),
                                 "rb"))

    def view_polls(self, request: HttpRequest) -> HttpResponse:
        """Display a list of polls."""
        now = timezone.now()
        polls = list(
            Poll.objects.filter(pub_date__lte=now).order_by("-pub_date")[:100])
        return render(
            request, "index.html", {
                "data":
                dumps([{
                    "id": poll.id,
                    "name": poll.name,
                    "image": poll.image,
                    "open": poll.end_date is None or poll.end_date >= now
                } for poll in polls])
            })

    def view_create(self,
                    request: HttpRequest,
                    poll_id: int = None) -> HttpResponse:
        """Display the poll creator view."""
        user = check_auth(request)
        if user is None:
            return redirect("polls:auth")
        if poll_id is not None:
            poll = get_or_none(Poll, id=poll_id)
            if poll is None:
                messages.add_message(request, messages.ERROR,
                                     "Poll not found.")
                return render(request, "error_message.html",
                              {"header": "Failed to load poll"})
        return FileResponse(
            open(FRONTEND.joinpath("create", "index.html"), "rb"))

    def view_poll(self, request: HttpRequest, poll_id: int) -> HttpResponse:
        """Return the html file for viewing the poll."""
        poll = get_or_none(Poll, id=poll_id)
        if poll is None:
            messages.add_message(request, messages.ERROR, "Poll not found.")
            return render(request, "error_message.html",
                          {"header": "Failed to load poll"})
        user = check_auth(request)
        prev_answers = []
        if user is not None:
            prev_answers = list(
                Response.objects.filter(submitter=user,
                                        question=poll).values("key", "value"))
            print(prev_answers)
        return render(
            request, "poll/index.html", {
                "data":
                dumps({
                    "req_auth": user is None and poll.requires_auth(),
                    "is_creator": user is not None and poll.creator == user,
                    "can_vote": poll.can_vote(user),
                    "can_res": poll.can_view_responses(user),
                    "closed": poll.is_closed(),
                    "prev_ans": prev_answers,
                    "id": poll_id,
                    "yaml": poll.yaml if poll.can_view(user) else None
                })
            })

    def view_res(self, request: HttpRequest, poll_id: int) -> HttpResponse:
        """Return the html file for results."""
        poll = get_or_none(Poll, id=poll_id)
        if poll is None:
            messages.add_message(request, messages.ERROR, "Poll not found.")
            return render(request, "error_message.html",
                          {"header": "Failed to load poll responses"})
        user = check_auth(request)
        if not poll.can_view_responses(user):
            messages.add_message(
                request, messages.ERROR, "You do not have permission to"
                "view the responses of this poll.")
            return render(request, "error_message.html",
                          {"header": "Access denied"})
        return render(
            request, "res/index.html", {
                "data":
                dumps({
                    "can_view": poll.can_view(user),
                    "can_edit": user is not None and user == poll.creator,
                    "responses": poll.get_responses(),
                    "yaml": poll.yaml,
                    "id": poll_id
                })
            })
