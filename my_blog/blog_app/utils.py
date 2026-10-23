import logging
import deepl
from django.conf import settings

logger = logging.getLogger(__name__)

CODES_CIBLE = {"fr": "FR", "en": "EN-US"}


def traduire(texte, source, cible):
    if not texte:
        return ""
    try:
        translator = deepl.Translator(settings.DEEPL_API_KEY)
        resultat = translator.translate_text(texte,source_lang=source.upper(),target_lang=CODES_CIBLE[cible])
        return resultat.text or ""
    except Exception:
        logger.exception("Traduction échouée (%s -> %s)", source, cible)
        return ""

# Fonction pour traduire automatiquement les champs spécifiés d'une instance de modèle (généré par ia: ChatGPT)
def auto_traduire(sender, instance, champs):
    ancien = sender.objects.filter(pk=instance.pk).first() if instance.pk else None

    for champ in champs:
        valeurs = {}
        modifies = []

        for lang in ("fr", "en"):
            nom = f"{champ}_{lang}"
            actuel = getattr(instance, nom, None) or ""
            avant = (getattr(ancien, nom, None) or "") if ancien else ""
            valeurs[lang] = actuel
            if actuel != avant:
                modifies.append(lang)

        if len(modifies) == 1:
            # Une seule langue modifiée (ou créée) : c'est la source
            source = modifies[0]
        elif not modifies:
            # Rien de modifié : on ne comble que une version manquante
            source = "fr" if valeurs["fr"] else "en"
            cible = "en" if source == "fr" else "fr"
            if not valeurs[source] or valeurs[cible]:
                continue
        else:
            # Les deux langues modifiées à la main : on respecte la saisie
            continue

        cible = "en" if source == "fr" else "fr"
        resultat = traduire(valeurs[source], source, cible)

        # On n'écrase la version existante que si la traduction a réussi
        if resultat:
            setattr(instance, f"{champ}_{cible}", resultat)