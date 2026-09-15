from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=50, verbose_name="nom")
  password = models.CharField(max_length=200, verbose_name="mdp")
  email = models.CharField(max_length=50, verbose_name="email")
  is_admin = models.BooleanField(verbose_name="admin")


  class Meta:
    ordering = ('name','email','password','is_admin', )
    verbose_name = "utilisateur"
    verbose_name_plural = "utilisateurs"

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
  categories = models.ManyToManyField('Category', verbose_name="Catégorie", related_name='products')

  class Meta:
    ordering = ('title','description','imageUrl','creator','createAt', )
    verbose_name = "publication"
    verbose_name_plural = "publications"