from django.views.generic.base import View
from django.core.paginator import Paginator
from ..models import Category, Post
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

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

        return render(request, "blog_app/post/post_list.html", context)
    
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

        return render(request, "blog_app/post/post.html", context)

class CreatePostView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        categories = Category.objects.all()

        context = {
            "categories": categories,
        }

        return render(request, "blog_app/post/post_create.html", context)

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
            return render(request, "blog_app/post/post_create.html", context)

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
            
            return render(request, "blog_app/post/post_edit.html", context)
    
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
                return render(request, "blog_app/post/post_edit.html", context)
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
        return render(request, "blog_app/post/post_delete.html", context)
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

        post.delete()
        messages.success(request, "Le post a été supprimé.")
        return redirect("profile")
