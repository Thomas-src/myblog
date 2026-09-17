from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=50, verbose_name="Nom")

  def __str__(self):
    return self.name

  class Meta:
    ordering = ('name', )
    verbose_name = "catégorie"
    verbose_name_plural = "catégories"


class Post(models.Model):
  title = models.CharField(max_length=50, verbose_name="titre")
  description = models.CharField(max_length=500, verbose_name="description")
  imageUrl = models.CharField(max_length=100, verbose_name="lien image")
  createAt = models.DateTimeField(verbose_name="date de création", auto_now_add=True)
  creator = models.ForeignKey(User, verbose_name="Utilisateur", related_name='posts', on_delete=models.CASCADE)
  categories = models.ManyToManyField('Category', verbose_name="Catégorie", related_name='categories')

  class Meta:
    ordering = ('title','description','imageUrl','creator','createAt', )
    verbose_name = "publication"
    verbose_name_plural = "publications"