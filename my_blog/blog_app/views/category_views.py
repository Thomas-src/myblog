from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator
from ..models import Category, Post
from ..forms import CategoryForm
from django.conf import settings

from django.utils import timezone

from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
class CategoryView(DetailView):
    model = Category
    template_name = "blog_app/category/category.html"
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class CategoryListView(ListView):
    model = Category
    paginate_by = 18
    template_name = "blog_app/category/category_list.html"
    ordering = ["name"]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class CategoryEditView(View):
    model = Category
    template_name = "blog_app/category/category_edit.html"
    form_class = CategoryForm
    fields = ["name"]
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        try:
            category = Category.objects.get(id=id)

        except Category.DoesNotExist:
            messages.error(request,"La catégorie n'existe pas")
            return redirect("category_list")

        form = CategoryForm(instance=category)

        context = {
            "form": form,
            "category": category,
            "action_text": "Enregistrer",
        }

        return render(
            request,
            "blog_app/category/category_edit.html",
            context
        )

    def post(self, request, id):

        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        try:
            category = Category.objects.get(id=id)

        except Category.DoesNotExist:
            messages.error(request, "La catégorie n'existe pas")
            return redirect("category_list")

        
        form = CategoryForm( request.POST,instance=category)

        if form.is_valid():
            category = form.save()

            messages.success(request,f'Catégorie "{category.name}" modifiée avec succès.')

            return redirect("category",id=category.id)

        context = {
            "form": form,
            "category": category,
            "action_text": "Enregistrer",
        }

        return render(request,"blog_app/category/category_edit.html",context)

class CreateCategoryView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        form = CategoryForm()
        context = {
            "form": form,
        }
        return render(request, "blog_app/category/category_create.html", context)

    def post(self, request):
            # Vérifier connexion utilisateur
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            
            form = CategoryForm(request.POST)
            
            if form.is_valid():
                name = form.cleaned_data["name"]
                category = form.save()
                messages.success(request, f"Catérorie \"{name}\" ajoutée avec succès.")
                return redirect("category", id=category.id)

            context = {
            'action_text': 'Ajouter',
            'form': form
            }
            return render(request, "blog_app/category/category_create.html", context)
        
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
        return render(request, "blog_app/category/category_delete.html", context)
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
