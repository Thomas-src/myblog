from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),

    path('post/list/', views.PostListView.as_view(), name="post_list"),
    path('post/<int:id>/', views.PostView.as_view(), name="post"),
    path('post/create/', views.CreatePostView.as_view(), name="post_create"),
    path('post/edit/<int:id>/', views.EditPostView.as_view(), name="post_edit"),
    path('post/delete/<int:id>/', views.DeletePostView.as_view(), name='post_delete'),

    path('category/list/', views.CategoryListView.as_view(), name="category_list"),
    path('category/<int:pk>/', views.CategoryView.as_view(), name="category"),
    path('category/create/', views.CreateCategoryView.as_view(), name='category_create'),
    path('category/edit/<int:pk>/', views.CategoryEditView.as_view(), name="category_edit"),
    path('category/delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='category_delete'),

    path('user/<int:id>/', views.UserView.as_view(), name="user"),


    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='profile'),
]

