from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator
from ..models import Category, Post
from ..forms import CategoryForm
from django.conf import settings

from django.utils import timezone

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
class CategoryView(DetailView):
    model = Category
    template_name = "blog_app/category/category.html"
    paginate_by = 6
    def get_context_data(self, **kwargs):
        category = self.object
        context = super().get_context_data(**kwargs)
        context["posts"] = category.posts.all()
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

class CategoryEditView(PermissionRequiredMixin,UpdateView):
    permission_required = "blog_app.change_category"
    model = Category
    template_name = "blog_app/category/category_edit.html"
    form_class = CategoryForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_text"] = "Modifier"
        return context
    def form_valid(self, form):
        category = form.save()

        messages.success(self.request,f'Catégorie "{category.name}" modifiée avec succès.')

        return redirect("category", pk=category.pk)

class CreateCategoryView(PermissionRequiredMixin,CreateView):
    permission_required = "blog_app.add_category"
    template_name = "blog_app/category/category_create.html"
    model = Category
    form_class = CategoryForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_text"] = "Créer"
        return context
    def form_valid(self, form):
        category = form.save()

        messages.success(self.request,f'Catégorie "{category.name}" créée avec succès.')

        return redirect("category", pk=category.pk)

class DeleteCategoryView(PermissionRequiredMixin,DeleteView):
    permission_required = "blog_app.delete_category"
    model = Category
    template_name = "blog_app/category/category_delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_text"] = "Supprimer"
        return context
    def form_valid(self, form):
        category = self.object

        if category.posts.exists():
            messages.error(self.request,"La catégorie ne peut pas être supprimée, ""elle est liée à un ou plusieurs posts.")
            return redirect("category_list")

        category.delete()

        messages.success(self.request,"La catégorie a été supprimée.")

        return redirect("category_list")