from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User, Group
from .models import Post, Category
from .utils import auto_traduire

# Gestion d'images

# Signal pour supprimer l'image associée à un post lorsque le post est supprimé
@receiver(post_delete, sender=Post)
def post_post_delete(sender, instance, **kwargs):
  instance.image.delete(False) # Passez False pour ne pas enregistrer le modèle.

# Signal pour supprimer l'ancienne image d'un post lorsque l'image est modifiée
@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
  if instance.pk:
    try:
      old_image = sender.objects.get(pk=instance.pk).image
      if old_image != instance.image:
        old_image.delete(False) # Passez False pour ne pas enregistrer le modèle.
    except Post.DoesNotExist:
      pass

# Gestion de groupes

# Signal pour ajouter un groupe à un utilisateur nouvellement créé
@receiver(post_save, sender=User)
def ajouter_groupe_utilisateur(sender, instance, created, **kwargs):
    if created:
      print(Group.objects.filter(name="user").exists())
      groupe, _ = Group.objects.get_or_create(name="user")
      instance.groups.add(groupe)
      print(f"Groupe {groupe.name} ajouté à {instance.username}")

# Traduction automaitque

# Signal pour traduire automatiquement le nom d'une catégorie
@receiver(pre_save, sender=Category)
def category_pre_save_traduction(sender, instance, **kwargs):
  auto_traduire(sender, instance, ("name",))


# Signal pour traduire automatiquement le titre et la description d'un post
@receiver(pre_save, sender=Post)
def post_pre_save_traduction(sender, instance, **kwargs):
  auto_traduire(sender, instance, ("title", "description"))