from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from .models import Category, Post

# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "view_products_link"]
    ordering = ['name',]
    readonly_fields = ("products_list",)
    search_fields = ["name","products_list"]
    def products_list(self, obj):
        if not obj.pk:
            return "-"
        
        products = obj.products.all()
        if not products:
            product_links = "Aucun produit associé"
        else:
            product_links = format_html_join(
                mark_safe("<br>"),
                '<a href="{}">{}</a>',
                (
                    (
                        reverse("admin:demo_app_product_change", args=[p.pk]),
                        p.name,
                    )
                    for p in products
                )
            )

        # Lien pour ajouter un produit avec la catégorie pré-remplie
        add_url = (reverse("admin:demo_app_product_add")+ f"?category={obj.pk}")
        add_link = format_html( '<br><br><a class="addlink" href="{}">Ajouter un produit</a>',add_url)

        return format_html("{}{}", product_links, add_link)

    products_list.short_description = "Produits associés"

    def view_products_link(self, obj):
        url = (reverse("admin:demo_app_product_changelist")+ f"?category__id__exact={obj.id}")
        return format_html('<a href="{}">Voir les produits</a>', url)

    view_products_link.short_description = "Produits associés"



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description','image','createAt', 'creator',]
    list_filter = ['categories','creator',]
    ordering = ['createAt',]
    readonly_fields = ['id']
    search_fields = ['id', 'name', 'title','description',]
