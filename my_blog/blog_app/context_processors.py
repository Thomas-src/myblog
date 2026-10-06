from .models import Category, Post

def categories_processor(request):
  return { "all_categories": Category.objects.all() }
  
def posts_processor(request):
  return { "all_posts": Post.objects.all() }