from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   UpdateModelMixin)

from common.permissions import IsOwnerOrAdmin

from .models import Group, SendGroupInvite
from .serializers import (GroupListSerializer, GroupSerializer,
                          SendGroupInviteCreateSerializer,
                          SendGroupInviteListSerializer,
                          SendGroupInviteUpdateSerializer)


class GroupViewset(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]

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
        request.data['sending_username'] = request.user.username
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.accepted:
            group = instance.group
            group.members.add(instance.receiving_username)
            group.save()
