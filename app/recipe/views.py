from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    ''' Manage tags in the database
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        ''' Return objects for the current authenticated user only '''
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        ''' Create a new tag '''
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    ''' Manage ingredient in the database
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        ''' Return objects for the current authenticated user only '''
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        ''' Create a new ingredient '''
        serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    ''' Manage reccipes in the database
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        ''' Return objects for the current authenticated user only '''
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        ''' Return appropiate serializer class'''
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        ''' Create a new recipe '''
        serializer.save(user=self.request.user)