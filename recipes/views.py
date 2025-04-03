from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin)

from common.permissions import IsOwnerOrAdmin
from recipes.models import Ingredient, Recipe, Step
from recipes.serializers import (IngredientSerializer, RecipeListSerializer,
                                 RecipeSerializer, RecipeUpdateSerializer,
                                 StepCreateSerializer, StepUpdateSerializer)


class IngredientViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner_username=self.request.user)


class StepViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Step.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return StepUpdateSerializer
        return StepCreateSerializer

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = get_object_or_404(Step, pk=pk)
        steps = instance.recipe.steps.order_by('step_number')

        for step in steps:
            if step.step_number > instance.step_number:
                step.step_number -= 1
                step.save()

        return super().destroy(request, *args, **kwargs)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrAdmin]
    search_fields = ['name']

    def get_queryset(self):
        return Recipe.objects.filter(owner_username=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        elif self.action in ['update', 'partial_update']:
            return RecipeUpdateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(owner_username=self.request.user)
