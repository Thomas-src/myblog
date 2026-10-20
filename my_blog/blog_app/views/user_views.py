

from ..models import Category, Post
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator

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

class EditUserProfileView(View):
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect("index")
        return render(request, "blog_app/user/edit-profile.html", context)
