from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator
from .models import Category, Post

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

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
    

# Posts views

class PostListView(View):
    paginate_by = 6
    def get(self, request):
      
        try:
            posts = Post.objects.all().order_by("-createAt")
        except Post.DoesNotExist:
            posts = None
        paginator = Paginator(posts, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))
        context = {
            "page_obj": page_obj,
        }

        return render(request, "blog_app/post_list.html", context)
    
class PostView(View):
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request, "Le poste n'existe pas")
            return redirect("post_list")
        
        context = {
            "post": post,
            "post_categories" : post.categories.all().order_by("-id")
        }

        return render(request, "blog_app/post.html", context)

class CategoryEditView(View):
    def get(self, request, id):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            messages.error(request,"La catégorie n'existe pas")
            redirect("category_list")
        

        context = {
            "category": category,
        }

        return render(request, "blog_app/category_edit.html", context)

    def post(self, request, id):
                # Vérifier connexion utilisateur
                if not request.user.is_authenticated:
                    return redirect(f"{settings.LOGIN_URL}?next={request.path}")
                
                try:
                    category = Category.objects.get(id=id)
                except Category.DoesNotExist:
                     messages.error(request,"La catégorie n'existe pas")
                     return redirect("category_list")
                
                category_name = request.POST.get("category_name", "").strip()
    
                if not category_name:
                        context =  {"category_name": category_name,"category": category,}
                        messages.error(request,"Le nom de la nouvelle catégorie est obligatoire")
                        return render(request,"blog_app/category_create.html",context)
                # TODO verifier si categorie existe deja
                category.name = category_name
                category.save()
                messages.success(request,"Catégorie modifiée avec succès")
                return redirect("category", id=category.id)

class CreatePostView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        categories = Category.objects.all()

        context = {
            "categories": categories,
        }

        return render(request, "blog_app/post_create.html", context)

    def post(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            context = {
            "categories": Category.objects.all(),
            "form": {"title": "", "description": "", "image": "", "categories": []},
            }
            return redirect(f"{settings.LOGIN_URL}?next={request.path}",context)
        
        # Récupérer anciennes données nettoyées ??? XSS
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")
        category_ids = request.POST.getlist("categories")

        categories = Category.objects.all()

        # Vérifier données reauises
        title = request.POST.get("title", "").strip()
        if not title or not description:
            messages.error(request,"Le titre et la description sont obligatoires.")
            context = {
                "categories": categories,
                "form": {
                    "title":title,
                    "description":description,
                    "image":image,
                    "category_ids":category_ids
                }
            }
            return render(request, "blog_app/post_create.html", context)

        title = request.POST.get("title", "").strip()
        post = Post.objects.create(
            title=title,
            description=description,
            image=image,
            creator=request.user,
        )
        if category_ids:
            post.categories.set(category_ids)

        messages.success(request,"Le post a été créé avec succès")
        return redirect("post", id=post.id)

class EditPostView(View):
     def get(self, request,id):
            # Vérifier connexion utilisateur
            try:
                post = Post.objects.get(id=id)
            except Post.DoesNotExist:
                messages.error(request,"Le post n'existe pas")
                return redirect("profile")

            if post.creator != request.user:
                messages.error(request, "Vous ne pouvez modifier que vos propres posts")
                return redirect("profile")

            context = {  "post": post,
                       "categories": Category.objects.all(),
                       "selected_ids": list(post.categories.values_list("id", flat=True)), }
            
            return render(request, "blog_app/post_edit.html", context)
    
     def post(self, request,id):
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

            try:
                post = Post.objects.get(id=id)
            except Post.DoesNotExist:
                messages.error(request,"Le post n'existe pas")
                return redirect("profile")
          
            if post.creator != request.user:
                messages.error(request, "Vous ne pouvez modifier que vos propres posts")
                return redirect("profile")

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            image = request.FILES.get("image")
            category_ids = request.POST.getlist("categories")

            if not title or not description:
                messages.success(request,"Le titre et la description sont obligatoire")
                context = {
                "post": post,
                "categories": Category.objects.all(),
                "form": {"title": title, "description": description},
                "selected_ids": list(post.categories.values_list("id", flat=True)),
                }
                return render(request, "blog_app/post_edit.html", context)
            post.title = title
            post.description = description

            if image:
                if post.image:
                        post.image.delete(save=False)
                post.image = image

            post.save()
            post.categories.set(category_ids)
            messages.success(request,"Le post a été modifié avec succès")
            return redirect("post", id=post.id)

class DeletePostView(View):
    def get(self, request,id):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request,"Le post n'existe pas")
            return redirect("profile")

        if post.creator != request.user:
            messages.error(request, "Vous ne pouvez modifier que vos propres posts")
            return redirect("profile")
        
        context = {  "post": post }
        return render(request, "blog_app/post_delete.html", context)
    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request,"Le post n'existe pas")
            return redirect("profile")
        
        if post.creator != request.user:
            messages.error(request, "Vous ne pouvez modifier que vos propres posts")
            return redirect("profile")

        if post.image:
            post.image.delete(save=False)

        post.delete()
        messages.success(request, "Le post a été supprimé.")
        return redirect("profile")

# User views

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

        return render(request, "blog_app/user.html", context)

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

        return render(request, "blog_app/profile.html", context)

# Category views

class CategoryView(View):
    paginate_by = 6
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            messages.error(request, "La catégorie n'existe pas")
            return redirect("category_list")
        
        posts = category.posts.all().order_by("-createAt")
        paginator = Paginator(posts, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))
        context = {
            "category": category,
            "page_obj":page_obj,
        }

        return render(request, "blog_app/category.html", context)

class CategoryListView(View):
    paginate_by = 18
    def get(self, request):
        categories = Category.objects.all()
        paginator = Paginator(categories, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))

        context = {
            "page_obj": page_obj,
        }

        return render(request, "blog_app/category_list.html", context)
     
class CreateCategoryView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return render(request, "blog_app/category_create.html")

    def post(self, request):
            # Vérifier connexion utilisateur
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
            category_name = request.POST.get("category_name", "").strip()

            if not category_name:
                    context =  {"category_name": category_name, }
                    messages.error(request,"Le nom de la nouvelle catégorie est obligatoire")
                    return render(request,"blog_app/category_create.html",context)
            # TODO verifier si categorie existe deja
            category = Category.objects.create(name=category_name)
            messages.success(request,"Catégorie créée avec succès")
            return redirect("category", id=category.id)
        
class DeleteCategoryView(View):
    def get(self, request,id):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            messages.error(request,"La catégorie n'existe pas")
            return redirect("category_list")
        
        if category.posts.exists():
            messages.error(request,"La catégorie ne peut pas être supprimée, elle est liée à plus d'un post")
            return redirect("category_list")
        
        context = {  "category": category }
        return render(request, "blog_app/category_delete.html", context)
    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            messages.error(request,"La catégorie n'existe pas")
            return redirect("category_list")
        
        if category.posts.exists():
            messages.error(request,"La catégorie ne peut pas être supprimée, elle est liée à plus d'un post")
            return redirect("category_list")
        
        category.delete()
        messages.success(request, "La catégorie a été supprimé.")
        return redirect("category_list")

# Account views
              
class loginview(View):
    def post(self,request):
         
        user = authenticate(request, username=request.POST["username"],password=request.POST["password"])

        if user:
            login(request, user)
        return redirect("index")
    
class SignUpView(View):
    def  post(self,request):
        if request.user.is_authenticated:
                    return redirect("profile")
        
        return render(request, "blog_app/index.html")

class LogoutView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        logout(request)
        return redirect("index")