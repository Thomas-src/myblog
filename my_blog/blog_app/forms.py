from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Category, Post
INPUT_CLASS = "w-full border border-gray-300 px-3 py-2 text-sm text-gray-900 focus:outline-none focus:border-gray-900"

class CategoryForm(forms.ModelForm):
  template_name = "blog_app/snippets/form_snippet.html"

  class Meta:
    model = Category
    fields = ['name_fr', 'name_en']
    widgets = {
            "name_fr": forms.TextInput(
                attrs={
                    "class":INPUT_CLASS
                }
            ),
             "name_en": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS
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

 
class EditUserProfileForm(forms.ModelForm):
  old_password = forms.CharField(
    label=_("Mot de passe actuel"),
    widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "autocomplete": "current-password"}),
  )
  new_password1 = forms.CharField(
    label=_("Nouveau mot de passe"),
    required=False,
    widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "autocomplete": "new-password"}),
  )
  new_password2 = forms.CharField(
    label=_("Confirmation du nouveau mot de passe"),
    required=False,
    widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "autocomplete": "new-password"}),
  )

  class Meta:
    model = User
    fields = ["username"]
    labels = {"username": _("Nom d'utilisateur")}
    widgets = {
      "username": forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "username"}),
    }

  def clean_old_password(self):
    old_password = self.cleaned_data["old_password"]
    if not self.instance.check_password(old_password):
      raise ValidationError(_("Le mot de passe actuel est incorrect."))
    return old_password

  def clean(self):
    cleaned = super().clean()
    p1 = cleaned.get("new_password1")
    p2 = cleaned.get("new_password2")

    if p1 or p2:
      if p1 != p2:
        self.add_error("new_password2", _("Les deux mots de passe ne correspondent pas."))
      else:
        try:
          password_validation.validate_password(p1, self.instance)
        except ValidationError as e:
          self.add_error("new_password1", e)
    return cleaned

  def save(self, commit=True):
    user = super().save(commit=False)
    new_password = self.cleaned_data.get("new_password1")
    if new_password:
      user.set_password(new_password)
    if commit:
      user.save()
    return user