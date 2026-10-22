import logging
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

def traduire(texte, source, cible):
    if not texte:
        return ""
    try:
        return GoogleTranslator(source=source, target=cible).translate(texte) or ""
    except Exception as e:
        print(f"[TRADUCTION ÉCHOUÉE] {type(e).__name__}: {e}")
        return ""

# Fonction pour traduire automatiquement les champs spécifiés d'une instance de modèle (généré par ia: ChatGPT)
def auto_traduire(sender, instance, champs):
  # Ancienne version en base (None si c'est une création)
  ancien = None
  if instance.pk:
    ancien = sender.objects.filter(pk=instance.pk).first()

  for champ in champs:
    fr = getattr(instance, f"{champ}_fr", None)
    en = getattr(instance, f"{champ}_en", None)
    fr_avant = getattr(ancien, f"{champ}_fr", None) if ancien else None
    en_avant = getattr(ancien, f"{champ}_en", None) if ancien else None

    fr_modifie = fr != fr_avant
    en_modifie = en != en_avant

    if fr and (not en or (fr_modifie and not en_modifie)):
      # FR nouveau ou modifié, EN vide ou pas touché : FR -> EN
      setattr(instance, f"{champ}_en", traduire(fr, "fr", "en"))
    elif en and not fr:
      # EN seulement : EN -> FR
      setattr(instance, f"{champ}_fr", traduire(en, "en", "fr"))