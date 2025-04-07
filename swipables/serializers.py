from rest_framework import serializers

from groups.models import Group

from .models import Swipe


class SwipeSerializer(serializers.ModelSerializer):
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)

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
