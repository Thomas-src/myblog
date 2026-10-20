from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from ..models import Category, Post
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from ..forms import PostForm
class PostListView(ListView):
    model = Post
    paginate_by = 6
    template_name = "blog_app/post/post_list.html"
    ordering = ["-createAt"]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class PostView(DetailView):
    model = Post
    template_name = "blog_app/post/post.html"
    def get_context_data(self, **kwargs):
        post = self.object
        context = super().get_context_data(**kwargs)
        context["post"] = post
        context["post_categories"] = post.categories.all().order_by("-id")
        return context

class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = "blog_app.add_post"
    model = Post
    form_class = PostForm
    template_name = "blog_app/post/post_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["action_text"] = "Créer"
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,"Le post a été créé avec succès.")
        return redirect("post", pk=self.object.pk)



class CreatePostView(PermissionRequiredMixin,View):
    permission_required = "blog_app.add_post"
    model = Post
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
        return redirect("post", pk=post.pk)


class EditPostView(PermissionRequiredMixin,UpdateView):
    permission_required = "blog_app.change_post"
    model = Post
    template_name = "blog_app/post/post_edit.html"
    form_class = PostForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_ids"] = list(self.object.categories.values_list("id", flat=True))
        context["action_text"] = "Modifier"
        return context
    def form_valid(self, form):
        post = self.object
        
        if post.creator != self.request.user:
            messages.error(self.request, "Vous ne pouvez modifier que vos propres posts")
            return redirect("profile")
        
        category = form.save()
        messages.success(self.request,f'Post "{category.pk}" modifié avec succès.')

        return redirect("post", pk=category.pk)


class DeletePostView(PermissionRequiredMixin,DeleteView):
    permission_required = "blog_app.delete_post"
    model = Post
    template_name = "blog_app/post/post_delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_text"] = "Supprimer"
        return context
    def form_valid(self, form):
        post = self.object

        # Uniquement le groupe admin peut le poste désormais
        # if post.creator != self.request.user:
        #    messages.error(self.request, "Vous ne pouvez modifier que vos propres posts")
        #    return redirect("profile")

        post.delete()

        messages.success(self.request,"Le post a été supprimé.")

        return redirect("profile")