from rest_framework import viewsets

from common.permissions import IsOwnerOrAdmin

from .models import Group
from .serializers import GroupListSerializer, GroupSerializer


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
