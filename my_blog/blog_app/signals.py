from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from .models import Post

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