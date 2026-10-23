

from ..models import Category, Post
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from ..forms import EditUserProfileForm


class UserView(View):
    paginate_by = 6
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            messages.error(request, "L'utilisateur n'existe pas")
            return redirect("index")

        posts = user.posts.all().order_by("-createAt")
        paginator = Paginator(posts, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))
        context = {
            "user": user,
            "page_obj":page_obj,
        }

        return render(request, "blog_app/user/profile.html", context)

class UserProfileView(View):
    paginate_by = 6

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect("index")

        posts = user.posts.all().order_by("-createAt")
        paginator = Paginator(posts, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))
        context = {
            "user": user,
            "page_obj":page_obj,
        }

        return render(request, "blog_app/user/profile.html", context)

class EditUserProfileView(LoginRequiredMixin, View):
    template_name = "blog_app/user/edit-profile.html"

    def get_user(self, request):
        return User.objects.get(pk=request.user.pk)

    def get(self, request):
        form = EditUserProfileForm(instance=self.get_user(request))
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EditUserProfileForm(request.POST, instance=self.get_user(request))
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get("new_password1"):
                update_session_auth_hash(request, user)
            messages.success(request, _("Votre profil a été mis à jour."))
            return redirect("profile")
        return render(request, self.template_name, {"form": form})