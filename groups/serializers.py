from rest_framework import serializers

from users.serializers import UserListSerializer

from .models import Group, SendGroupInvite


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'owner_username', 'member_count']


class GroupSerializer(serializers.ModelSerializer):
    members = UserListSerializer(many=True, read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    owner_username = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        exclude = ['composite_key', 'created', 'modified']

    def validate_name(self, value):
        request_user = self.context['request'].user
        if Group.objects.filter(owner_username=request_user, name=value).exists():
            raise serializers.ValidationError(
                "A group with this name already exists.")
        return value


class SendGroupInviteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGroupInvite
        exclude = ['composite_key', 'created', 'modified']


class SendGroupInviteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendGroupInvite
        exclude = ['accepted', 'composite_key', 'created', 'modified']

    def validate(self, data):
        request_user = self.context['request'].user
        if SendGroupInvite.objects.filter(
                sending_username=request_user,
                group=data['group'],
                receiving_username=data['receiving_username']
        ).exists():
            raise serializers.ValidationError(
                "An invite to this user for this group already exists.")
        return data
