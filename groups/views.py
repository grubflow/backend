from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from common.permissions import IsOwnerOrAdmin

from .models import Group, SendGroupInvite
from .serializers import (GroupListSerializer, GroupSerializer,
                          SendGroupInviteCreateSerializer,
                          SendGroupInviteListSerializer)


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        group = serializer.save(owner_username=self.request.user)
        group.members.add(self.request.user)
        group.save()


class SendGroupInviteViewset(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = SendGroupInvite.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SendGroupInviteListSerializer
        return SendGroupInviteCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['sending_username'] = request.user.username
        return super().create(request, *args, **kwargs)
