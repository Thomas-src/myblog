from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "view_posts_link"]
    ordering = ["name"]
    readonly_fields = ["posts_list"]
    search_fields = ["name", "posts__title"]

    @admin.display(description="Publications associées")
    def posts_list(self, obj):
        if not obj.pk:
            return "-"

        posts = obj.posts.all()
        if posts:
            post_links = format_html_join(
                mark_safe("<br>"),
                '<a href="{}">{}</a>',
                (
                    (reverse("admin:blog_app_post_change", args=[p.pk]), p.title)
                    for p in posts
                ),
            )
        else:
            post_links = _("Aucune publication associée")

        # Lien pour ajouter une publication avec la catégorie pré-remplie
        add_url = reverse("admin:blog_app_post_add") + f"?categories={obj.pk}"
        add_link = format_html('<br><br><a class="addlink" href="{}">{}</a>',add_url,_("Ajouter une publication"),)

        return format_html("{}{}", post_links, add_link)

    @admin.display(description=_("Publications"))
    def view_posts_link(self, obj):
        url = (
            reverse("admin:blog_app_post_changelist")
            + f"?categories__id__exact={obj.pk}"
        )
        return format_html('<a href="{}">{}</a>', url, _("Voir les publications"))


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = [
        "title_with_image",
        "description",
        "image_preview",
        "createAt",
        "creator",
    ]
    list_filter = ["categories", "creator"]
    ordering = ["createAt"]
    readonly_fields = ["createAt"]
    search_fields = ["title", "description"]

    @admin.display(description="Titre")
    def title_with_image(self, obj):
        if obj.image:
            return format_html(
                '<span style="display:flex; align-items:center;">'
                '<img src="{}" style="max-width:32px; margin-right:6px;" />'
                "{}"
                "</span>",
                obj.image.url,
                obj.title,
            )
        return obj.title

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:200px" />', obj.image.url
            )
        return ""

    def get_readonly_fields(self, request, obj=None):
        # N'affiche la prévisualisation que lors de la modification
        if obj:
            return [*self.readonly_fields, "image_preview"]
        return self.readonly_fields