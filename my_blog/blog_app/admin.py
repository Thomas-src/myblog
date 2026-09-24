from django.contrib import admin
from .models import Category, Post
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    ordering = ['id',]
    readonly_fields = ['id']
    search_fields = ['id', 'name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description','image','createAt', 'creator',]
    list_filter = ['categories','creator',]
    ordering = ['createAt',]
    readonly_fields = ['id']
    search_fields = ['id', 'name', 'title','description',]
