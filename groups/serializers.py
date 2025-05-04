from rest_framework import serializers

from swipables.serializers import SwipableListSerializer
from users.serializers import UserListSerializer

from .models import Group, GroupFoodScore, SendGroupInvite


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'owner_username', 'member_count', 'capacity']


class GroupSerializer(serializers.ModelSerializer):
    members = UserListSerializer(many=True, read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)
    capacity = serializers.IntegerField(read_only=True)
    num_sessions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        exclude = ['composite_key', 'created', 'modified']

    def validate_name(self, value):
        request_user = self.context['request'].user
        if Group.objects.filter(owner_username=request_user, name=value).exists():
            raise serializers.ValidationError(
                "A group with this name already exists.")

        if value == request_user.username:
            raise serializers.ValidationError(
                "You cannot name a group the same as your username.")

        return value


class SendGroupInviteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGroupInvite
        exclude = ['composite_key', 'created', 'modified', 'accepted']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        image = instance.group.owner_username.image
        rep["owner_image"] = request.build_absolute_uri(
            image.url) if image else None

        return rep


class SendGroupInviteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGroupInvite
        exclude = ['accepted', 'composite_key', 'created', 'modified']

    def validate(self, data):
        request_user = self.context['request'].user
        receiving_username = data.get("receiving_username")
        group = data.get('group')

        if group.name == request_user.username:
            raise serializers.ValidationError(
                "You cannot invite users to your base group.")

        if request_user == receiving_username:
            raise serializers.ValidationError(
                "You cannot send an invite to yourself.")

        if not group or not Group.objects.filter(
            composite_key=group.composite_key,
            members=request_user
        ).exists():
            raise serializers.ValidationError(
                "You must be a member of the group to send an invite.")
        return data


class SendGroupInviteUpdateSerializer(serializers.ModelSerializer):
    sending_username = serializers.PrimaryKeyRelatedField(read_only=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    receiving_username = serializers.PrimaryKeyRelatedField(read_only=True)
    accepted = serializers.BooleanField(required=True)

    class Meta:
        model = SendGroupInvite
        exclude = ['composite_key', 'created', 'modified']

    def validate(self, data):
        request_user = self.context['request'].user
        if request_user != self.instance.receiving_username:
            raise serializers.ValidationError(
                "You are not authorized to accept or decline this invite.")
        if self.instance.accepted is not None or data.get('accepted') is None:
            raise serializers.ValidationError(
                "This invite has already been accepted or declined or is invalid.")
        return data


class GroupFoodScoreListSerializer(serializers.ModelSerializer):
    swipable = SwipableListSerializer(read_only=True)

    class Meta:
        model = GroupFoodScore
        fields = ['id', 'score', 'session', 'swipable']
