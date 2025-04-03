from rest_framework import serializers

from .models import Ingredient, Recipe, Step


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ["owner_username", "created", "modified"]

    def validate_name(self, value):
        lowercased_name = value.lower()
        if Ingredient.objects.filter(name__iexact=lowercased_name).exists():
            raise serializers.ValidationError(
                "ingredient with this name already exists.")
        return lowercased_name


class StepListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        exclude = ["created", "modified", "recipe"]


class StepUpdateSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    step_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Step
        exclude = ["created", "modified"]


class StepCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        exclude = ["created", "modified"]

    def validate_recipe(self, value):
        if value.owner_username != self.context["request"].user:
            raise serializers.ValidationError(
                "You do not have permission to add steps to this recipe.")
        return value


class StepCreateInternalSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Step
        exclude = ["created", "modified"]


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "description", "prep_time"]


class RecipeSerializer(serializers.ModelSerializer):
    steps = StepCreateInternalSerializer(many=True, required=True)
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ["created", "modified"]

    def validate_name(self, value):
        lowercased_name = value.lower()
        request_user = self.context["request"].user
        if Recipe.objects.filter(
            name__iexact=lowercased_name,
            owner_username=request_user
        ).exists():
            raise serializers.ValidationError(
                "recipe with this name already exists.")

        return lowercased_name

    def create(self, validated_data):
        steps_data = validated_data.pop("steps", [])
        ingredients_data = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        recipe.ingredients.set(ingredients_data)

        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["steps"] = StepListSerializer(
            instance.steps, many=True).data
        return representation


class RecipeUpdateSerializer(serializers.ModelSerializer):
    steps = StepListSerializer(many=True, read_only=True)
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ["created", "modified"]

    def validate_name(self, value):
        lowercased_name = value.lower()
        request_user = self.context["request"].user
        if Recipe.objects.filter(
            name__iexact=lowercased_name,
            owner_username=request_user
        ).exists() and self.context["request"].method not in ["PATCH", "PUT"]:
            raise serializers.ValidationError(
                "recipe with this name already exists.")

        return lowercased_name
