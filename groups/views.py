from django.shortcuts import get_object_or_404
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
        if self.action == "leave":
            permissions = [IsAuthenticated]
        else:
            permissions = [IsOwnerOrAdmin]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return GroupListSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        group = serializer.save(owner_username=self.request.user)
        group.members.add(self.request.user)
        group.save()

    @action(detail=True, methods=["delete"])
    def leave(self, request, pk=None):
        if not Group.objects.filter(composite_key=pk, members=request.user).exists():
            return Response({"detail": "You are not a member of this group."}, status=400)

        group_instance = Group.objects.get(composite_key=pk)
        group_instance.members.remove(request.user)
        group_instance.save()

        return Response(status=204)


class SendGroupInviteViewset(CreateModelMixin, ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        if self.action == "list":
            return SendGroupInvite.objects.filter(
                receiving_username=self.request.user, accepted__isnull=True)
        return SendGroupInvite.objects.filter(receiving_username=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return SendGroupInviteListSerializer
        elif self.action in ["update", "partial_update"]:
            return SendGroupInviteUpdateSerializer
        return SendGroupInviteCreateSerializer

    def create(self, request, *args, **kwargs):
        receiving_username = request.data.get("receiving_username")
        group = request.data.get("group")
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

        if hasattr(request.data, "_mutable"):
            setattr(request.data, "_mutable", True)
        request.data["sending_username"] = request.user.username
        return super().create(request, *args, **kwargs)

    def update(self, request, **kwargs):
        pk = kwargs.get("pk")
        instance = get_object_or_404(SendGroupInvite, pk=pk)
        serializer = self.get_serializer(
            instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        group = serializer.instance.group
        if serializer.instance.accepted:
            if group.member_count >= group.capacity:
                return Response({"detail": "Group is full."}, status=400)

            group.members.add(serializer.instance.receiving_username)
            group.save()

        return Response(serializer.data)
