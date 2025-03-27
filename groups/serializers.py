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
    group = GroupListSerializer()

    class Meta:
        model = SendGroupInvite
        fields = ['group']


class SendGroupInviteSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = SendGroupInvite
        fields = '__all__'
