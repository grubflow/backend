from rest_framework import serializers

from groups.models import Group
from recipes.serializers import RecipeListSerializer
from restaurants.serializers import RestaurantSerializer

from .models import Swipable, Swipe


class SwipeSerializer(serializers.ModelSerializer):
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)
    session = serializers.IntegerField(read_only=True)

    class Meta:
        model = Swipe
        exclude = ['created', 'modified']

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Score must be between 0 and 100.")
        return value

    def validate_group(self, value):
        request_user = self.context['request'].user
        if not Group.objects.filter(members=request_user).exists():
            raise serializers.ValidationError(
                "You must be a member of a group to swipe.")

        return value

    def validate(self, attrs):
        request_user = self.context['request'].user
        group = attrs.get('group')
        swipable = attrs.get('swipable')
        session = group.num_sessions

        if Swipe.objects.filter(
            owner_username=request_user,
            group=group,
            swipable=swipable,
            session=session
        ).exists():
            raise serializers.ValidationError(
                "You have already swiped this item in this group.")

        attrs['session'] = session

        return attrs


class SwipableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipable
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.recipe is not None:
            return {
                **(RecipeListSerializer(instance.recipe).data),
                **representation
            }

        if instance.restaurant is not None:
            return {
                **(RestaurantSerializer(instance.restaurant).data),
                **representation
            }
