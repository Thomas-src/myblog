from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View

from .models import User, Category, Post

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'blog_app/index.html')
    

class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()

        context = {
            'posts': posts,
        }

        return render(request, 'blog_app/post_list.html', context)
    

class PostView(View):
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
        
        context = {
            'post': post,
        }

        return render(request, 'blog_app/post.html', context)


class CategoryView(View):
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
        

        context = {
            'category': category,
        }

        return render(request, 'blog_app/category.html', context)

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()

        context = {
            'categories': categories,
        }

        return render(request, 'blog_app/category_list.html', context)
    


class UserView(View):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        
        context = {
            'user': user,
        }

        return render(request, 'blog_app/user.html', context)
    

class CreatePostView(View):
    def get(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        categories = Category.objects.all()

        context = {
            'categories': categories,
        }

        return render(request, 'blog_app/create_post.html', context)

    def post(self, request):
        # Vérifier connexion utilisateur
        if not request.user.is_authenticated:
            context = {
            'categories': Category.objects.all(),
            'form': {'title': '', 'description': '', 'image': '', 'categories': []},
            }
            return redirect(f"{settings.LOGIN_URL}?next={request.path}",context)
        
        # Récupérer anciennes données nettoyées ??? XSS
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.POST.get("image", "").strip()
        category_ids = request.POST.getlist("categories")

        categories = Category.objects.all()

        # Vérifier données reauises
        title = request.POST.get("title", "").strip()
        if not title or not description:
            context = {
                'categories': categories,
                'error': "Le titre et la description sont obligatoires.",
                'form': {
                    'title':title,
                    'description':description,
                    'image':image,
                    'category_ids':category_ids
                }
            }
            return render(request, 'blog_app/create_post.html', context)

        # Instancier l'objet
        title = request.POST.get("title", "").strip()
        post = Post.objects.create(
            title=title,
            description=description,
            imageUrl=image,
            creator=request.user,
        )
        # Ajouter l'objet
        if category_ids:
            post.categories.set(category_ids)

        return redirect('post', id=post.id)

class loginview(View):
    def post(self,request):
        user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('post_list')
        return render(request, 'blog_app/index.html')
    
class SignUpView(View):
    def  post(self,request):
        return render(request, 'blog_app/index.html')