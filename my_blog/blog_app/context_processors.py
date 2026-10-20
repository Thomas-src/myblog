from .models import Category, Post

def categories_processor(request):
  return { "all_categories": Category.objects.all() }
