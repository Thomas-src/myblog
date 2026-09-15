from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post/list/', views.PostListView.as_view(), name="post_list"),
    path('post/<int:id>/', views.PostView.as_view(), name="post"),

    path('category/list/', views.CategoryListView.as_view(), name="category_list"),
    path('category/<int:id>/', views.CategoryView.as_view(), name="category"),

      path('user/<int:id>/', views.UserView.as_view(), name="user"),
]
