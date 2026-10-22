from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Post

class CategoryForm(forms.ModelForm):
  template_name = "blog_app/snippets/form_snippet.html"

  class Meta:
    model = Category
    fields = ['name']
    widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
                }
            ),
        }
  
  def clean_name(self):
    name = self.cleaned_data['name']

    if self.instance.pk is None:
      name_exists = Category.objects.filter(name=name).exists()
    else:
      name_exists = Category.objects.filter(name=name).exclude(id=self.instance.pk).exists()

    if name_exists:
      raise ValidationError("Le nom de catégorie existe déjà")
    
    return name



class PostForm(forms.ModelForm):
  template_name = "blog_app/snippets/form_snippet.html"
  
  class Meta:
    model = Post
    fields = ['title', 'description', 'categories', 'image']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
      'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
      'image': forms.FileInput(attrs={'class': 'form-control'}),
    }

 