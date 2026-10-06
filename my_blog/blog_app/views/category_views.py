from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.core.paginator import Paginator
from ..models import Category, Post
from ..forms import CategoryForm
from django.conf import settings
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

        return render(request, "blog_app/category/category.html", context)

class CategoryListView(View):
    paginate_by = 18
    def get(self, request):
        categories = Category.objects.all()
        paginator = Paginator(categories, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))

        context = {
            "page_obj": page_obj,
        }

        return render(request, "blog_app/category/category_list.html", context)
     

class CategoryEditView(View):
    def get(self, request, id):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            messages.error(request,"La catégorie n'existe pas")
            return redirect("category_list")
        

        context = {
            "category": category,
        }

        return render(request, "blog_app/category/category_edit.html", context)

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
                context =  {"category_name": category_name,"category": category,}
                if not category_name:
                        
                        messages.error(request,"Le nom de la nouvelle catégorie est obligatoire")
                        return render(request,"blog_app/category/category_edit.html",context)
                # verifier si categorie existe deja
                if Category.objects.filter(name=category_name).exists():
                    messages.error(request, "Une catégorie avec ce nom existe déjà")
                    return render(request, "blog_app/category/category_edit.html", context)
               
                category.name = category_name
                category.save()
                messages.success(request,"Catégorie modifiée avec succès")
                return redirect("category", id=category.id)

class CreateCategoryView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return render(request, "blog_app/category/category_create.html")

    def post(self, request):
            # Vérifier connexion utilisateur
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            
            category_name = request.POST.get("category_name", "").strip()
            context =  {"category_name": category_name, }
            if not category_name:
                    
                    messages.error(request,"Le nom de la nouvelle catégorie est obligatoire")
                    return render(request,"blog_app/category/category_create.html",context)
             # verifier si categorie existe deja
            if Category.objects.filter(name=category_name).exists():
                messages.error(request, "Une catégorie avec ce nom existe déjà")
                return render(request, "blog_app/category/category_create.html", context)
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
