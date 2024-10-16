import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from homebin.users.models import SuperuserCreationFlag, User

logger = logging.getLogger(__name__)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


def create_superuser(request: HttpRequest):
    """UNSAFE VIEW: Create a superuser if none exists."""
    if SuperuserCreationFlag.objects.count() > 1:
        msg = "There should be only one SuperuserCreationFlag instance."
        raise ValueError(msg)
    flag = SuperuserCreationFlag.objects.first()
    if flag is not None and flag.created:
        return HttpResponseNotFound("Superuser already created.")

    if not User.objects.exists():
        superuser_email = "admin@example.com"
        superuser_password = "adminpassword"  # noqa: S105
        User.objects.create_superuser(
            email=superuser_email, password=superuser_password
        )

        if not flag:
            flag = SuperuserCreationFlag(created=True)
        else:
            flag.created = True
        flag.save()

        logger.info(
            "Superuser <%s> created. Password: %s", superuser_email, superuser_password
        )

        return HttpResponse(
            f"Superuser <{superuser_email}> created; see logs for info."
        )

    return HttpResponseNotFound("Superuser already exists or users already present.")
