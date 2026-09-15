from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View

from .models import User, Category, Post
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'blog_app/index.html')
    

class PostListView(View):
    def get(self, request):
        posts = Category.objects.all()

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