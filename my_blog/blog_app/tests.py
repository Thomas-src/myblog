from django.test import TestCase
from unittest.mock import patch
from blog_app.models import Category, Post
from django.contrib.auth.models import User
from django.urls import reverse
from blog_app.forms import EditUserProfileForm

# Create your tests here.

class ModelsTest(TestCase):
    def setUp(self):
        patcher = patch("blog_app.utils.traduire", return_value="x")
        patcher.start()
        
        self.addCleanup(patcher.stop)
        self.user = User.objects.create_user("thomas12345", password="Test1234$")

    def test_category_str(self):
        category = Category.objects.create(name="Cuisine")

        self.assertEqual(str(category), "Cuisine")

    def test_post_creation(self):
        post = Post.objects.create(title="IT conference", description="An IT conference", creator=self.user)

        self.assertIsNotNone(post.createAt)
        self.assertEqual(self.user.posts.count(), 1)

    def test_post_categories(self):
        category = Category.objects.create(name="Cuisine")
        post = Post.objects.create(title="IT conference", description="An IT conference", creator=self.user)
        post.categories.add(category)

        self.assertEqual(category.posts.count(), 1)

class EditUserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("thomas12345", password="Test1234$")

    def test_ancien_mot_de_passe_incorrect(self):
        data = {"username": "thothomas12345", "old_password": "faux"}
        form = EditUserProfileForm(data, instance=self.user)

        self.assertFalse(form.is_valid())

    def test_changement_username_valide(self):
        data = {"username": "thomas123452", "old_password": "Test1234$"}
        form = EditUserProfileForm(data, instance=self.user)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().username, "thomas123452")


class PostListViewTest(TestCase):
    def setUp(self):
        patcher = patch("blog_app.utils.traduire", return_value="x")
        patcher.start()
        self.addCleanup(patcher.stop)
        self.user = User.objects.create_user("thomas12345", password="Test1234$")
        self.client.force_login(self.user)
        self.url = reverse("post_list")

    def test_liste_affiche_les_posts(self):
        Post.objects.create(title="IT conference", description="An IT conference", creator=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IT conference")

    def test_liste_vide(self):
        response = self.client.get(self.url)

        self.assertContains(response, "Aucun résultat")