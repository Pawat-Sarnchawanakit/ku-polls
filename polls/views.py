"""Contain views."""
# pylint: disable=broad-exception-caught
import logging
from typing import Optional, cast
from datetime import datetime
from pathlib import Path
from json import loads, dumps
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, FileResponse, HttpResponseBase
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import Poll, Response, get_or_none

logger = logging.getLogger("polls")

FRONTEND = Path(__file__).parents[1].joinpath("frontend", "dist")


def get_client_ip(request) -> str:
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Logging
@receiver(user_logged_in)
def on_user_login(request, user, **__) -> None:
    """Log when user logs in."""
    ip = get_client_ip(request)
    logger.info('User `%s` logged in via ip: %s', user, ip)


@receiver(user_logged_out)
def on_user_logout(request, user, **__) -> None:
    """Log when user logs out."""
    ip = get_client_ip(request)
    logger.info('User `%s` logged out via ip: %s', user, ip)


@receiver(user_login_failed)
def on_user_login_failed(request, credentials, **__) -> None:
    """Log when user failed to login."""
    ip = get_client_ip(request)
    logger.warning('Login failed for: %s via ip: %s', credentials, ip)


def check_auth(request: HttpRequest) -> Optional[User]:
    """Check whether the user is authenticated.

    Args:
        request (HttpRequest): The request to check.

    Returns:
        User | None: The user if authenticated or None.
    """
    user = get_user(request)
    if user.is_anonymous:
        return None
    return cast(User, user)


class RPCHandler(View):
    """Handle RPC requests."""

    def post(self, request: HttpRequest) -> HttpResponseBase:
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

    def fn_create(self,
                  request: HttpRequest,
                  y: str,
                  b: Optional[int | datetime] = None,
                  c: Optional[int | datetime] = None,
                  e: Optional[str] = None,
                  n: str = "Unnamed poll",
                  i: str = '',
                  a: int = 0,
                  r: int = 0) -> HttpResponseBase:
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
            cur_poll = get_or_none(Poll, pk=e)
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
            return HttpResponse(cur_poll.pk)
        cur_poll = Poll.objects.create(yaml=y,
                                       name=n,
                                       res=r,
                                       image=i,
                                       creator=user,
                                       pub_date=b,
                                       end_date=c,
                                       allow=a)
        return HttpResponse(cur_poll.pk)

    def fn_res(self, request: HttpRequest, n: str) -> HttpResponseBase:
        """Return the responses and it's count."""
        if not isinstance(n, str):
            return HttpResponse("Poll number must be a string.", status=400)
        user = check_auth(request)
        poll = get_or_none(Poll, pk=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        if not poll.can_view_responses(user):
            return HttpResponse("Forbidden", status=403)
        return HttpResponse(dumps(poll.get_responses()))

    def fn_aa(self, request: HttpRequest, n: str) -> HttpResponseBase:
        """Check whether the poll is already answered."""
        poll = get_or_none(Poll, pk=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        user = check_auth(request)
        if user is not None:
            if Response.objects.filter(submitter=user,
                                       question=poll).first() is not None:
                return HttpResponse("y")
            return HttpResponse("n")
        return HttpResponse("idk", status=401)

    def fn_submit(self, request: HttpRequest, n: str, r: Optional[dict] = None) -> HttpResponseBase:
        """Submit answers to database."""
        user = check_auth(request)
        poll = get_or_none(Poll, pk=n)
        if poll is None:
            return HttpResponse("Poll does not exist.", status=404)
        if not poll.can_vote(user):
            return HttpResponse("Forbidden", status=403)
        if user is not None:
            Response.objects.filter(question=poll, submitter=user).delete()
        ip = get_client_ip(request)
        logger.info(
            "User `%s` submitted a response for poll id `%s` via ip `%s`: %s",
            user.username if user is not None else "Anonymous", n, ip, str(r))
        ress = []
        for k, v in (r or {}).items():
            ress.append(Response(question=poll, key=k, value=v,
                                 submitter=user))
        Response.objects.bulk_create(ress)
        return HttpResponse("ok")

    def fn_get(self, request: HttpRequest, n: str) -> HttpResponseBase:
        """Get a poll."""
        user = check_auth(request)
        poll = get_or_none(Poll, pk=n)
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

    def get(self, request: HttpRequest, **kwargs) -> HttpResponseBase:
        """Accept GET request for basic views."""
        if request.resolver_match is not None:
            name = request.resolver_match.url_name
            method = f"view_{name}"
            if hasattr(self, method):
                return getattr(self, method)(request, **kwargs)
        return HttpResponse("Page not found.", status=404)

    def view_polls(self, request: HttpRequest) -> HttpResponseBase:
        """Display a list of polls."""
        now = timezone.now()
        polls = list(
            Poll.objects.filter(pub_date__lte=now).order_by("-pub_date"))
        return render(
            request, "index.html", {
                "data":
                dumps([{
                    "id": poll.pk,
                    "name": poll.name,
                    "image": poll.image,
                    "open": poll.end_date is None or poll.end_date >= now
                } for poll in polls])
            })

    def view_create(self,
                    request: HttpRequest,
                    poll_id: Optional[int] = None) -> HttpResponseBase:
        """Display the poll creator view."""
        user = check_auth(request)
        if user is None:
            return redirect("login")
        if poll_id is not None:
            poll = get_or_none(Poll, pk=poll_id)
            if poll is None:
                messages.add_message(request, messages.ERROR,
                                     "Poll not found.")
                return render(request, "error_message.html",
                              {"header": "Failed to load poll"})
        return FileResponse(
            open(FRONTEND.joinpath("create", "index.html"), "rb"))

    def view_poll(self, request: HttpRequest, poll_id: int) -> HttpResponseBase:
        """Return the html file for viewing the poll."""
        poll = get_or_none(Poll, pk=poll_id)
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
        return render(
            request, "poll/index.html", {
                "data":
                dumps({
                    "auth": user is not None,
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

    def view_res(self, request: HttpRequest, poll_id: int) -> HttpResponseBase:
        """Return the html file for results."""
        poll = get_or_none(Poll, pk=poll_id)
        if poll is None:
            messages.add_message(request, messages.ERROR, "Poll not found.")
            return render(request, "error_message.html",
                          {"header": "Failed to load poll responses"})
        user = check_auth(request)
        if not poll.can_view_responses(user):
            messages.add_message(
                request, messages.ERROR, "You do not have permission to"
                " view the responses of this poll.")
            return render(request, "error_message.html",
                          {"header": "Access denied"})
        return render(
            request, "res/index.html", {
                "data":
                dumps({
                    "auth": user is not None,
                    "can_view": poll.can_view(user),
                    "can_edit": user is not None and user == poll.creator,
                    "responses": poll.get_responses(),
                    "yaml": poll.yaml,
                    "id": poll_id
                })
            })


class RegisterView(CreateView):
    """View for registration/signup."""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
