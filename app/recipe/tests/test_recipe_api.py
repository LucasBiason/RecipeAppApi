from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')

# /api/recipe/recipes
# /api/recipe/recipes/1/

def detail_url(recipe_id):
    """ return recipe detail url """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    ''' Create and return asample recipe '''
    defaults = {
        'title' : 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

def sample_tag(user, name='Main course'):
    ''' Create and return asample tag '''
    return Tag.objects.create(user=user, name=name)

def sample_ingredients(user, name='Cinnamon'):
    ''' Create and return asample ingredient '''
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeApiTests(TestCase):
    ''' test public available recipes API '''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        ''' Test that login is required for retrieving tags '''
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    ''' test the authorized user recipes API '''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        ''' test retrieving recipes '''
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))

    def test_recipes_limited_to_user(self):
        ''' teste that recipes returned are for the authenticated user '''
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'password123'
        )
        recipe = sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe.title)

    def test_view_recipe_detail(self):
        """ test viewing detail recipe """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredients(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        