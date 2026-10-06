from ..models import Category, Post
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.conf import settings

class IndexView(View):
    def get(self, request):

        try:
            latest = Post.objects.latest("createAt")
        except Post.DoesNotExist:
            latest = None

        context = {
            "latest_post": latest
        }

        return render(request, "blog_app/index.html", context)


class loginview(View):
    def post(self,request):
        user = authenticate(request, username=request.POST["username"],password=request.POST["password"])

        if user:
            login(request, user)
        return redirect("index")
    
class SignUpView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profile")
        return render(request,"registration/signup.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("profile")

        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        if not username or not password:
            return render(request,"registration/signup.html",{"error": "Tous les champs sont obligatoires."})

        if User.objects.filter(username=username).exists():
            return render(request,"registration/signup.html",{"error": "Ce nom d'utilisateur existe déjà."})

        User.objects.create_user( username=username,password=password)
        user = authenticate(request, username=request.POST["username"],password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("profile")

        return redirect("login")

class LogoutView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        logout(request)
        return redirect("index")