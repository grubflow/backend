from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import IsOwnerOrAdmin

from .models import Group, SendGroupInvite
from .serializers import (GroupListSerializer, GroupSerializer,
                          SendGroupInviteCreateSerializer,
                          SendGroupInviteListSerializer,
                          SendGroupInviteUpdateSerializer)


class GroupViewset(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'leave':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsOwnerOrAdmin]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        group = serializer.save(owner_username=self.request.user)
        group.members.add(self.request.user)
        group.save()

    @action(detail=False, methods=['delete'])
    def leave(self, request):
        group = request.data.get('group', None)
        if not group:
            return Response({"detail": "group parameter is required."}, status=400)
        elif not Group.objects.filter(composite_key=group, members=request.user).exists():
            return Response({"detail": "You are not a member of this group."}, status=400)

        group_instance = Group.objects.get(composite_key=group)
        group_instance.members.remove(request.user)
        group_instance.save()

        return Response(status=204)


class SendGroupInviteViewset(CreateModelMixin, ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return SendGroupInvite.objects.filter(
                receiving_username=self.request.user, accepted__isnull=True)
        return SendGroupInvite.objects.filter(receiving_username=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SendGroupInviteListSerializer
        elif self.action in ['update', 'partial_update']:
            return SendGroupInviteUpdateSerializer
        return SendGroupInviteCreateSerializer

    def create(self, request, *args, **kwargs):
        receiving_username = request.data.get('receiving_username')
        group = request.data.get('group')
        existing_invite = SendGroupInvite.objects.filter(
            sending_username=request.user,
            group__composite_key=group,
            receiving_username__username=receiving_username,
        ).first()
        existing_group = Group.objects.filter(
            composite_key=group,
            members__username=receiving_username
        ).first()
        if existing_invite and not existing_group:
            existing_invite.delete()

        request.data['sending_username'] = request.user.username
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.accepted:
            group = instance.group
            group.members.add(instance.receiving_username)
            group.save()
