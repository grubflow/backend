from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.permissions import IsOwnerOrAdmin

from .models import User
from .serializers import UserSerializer


class UserViewset(CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['current', 'logout']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
            {'access': access, 'refresh': str(refresh)},
            status=status.HTTP_201_CREATED
        )

    @action(methods=['GET'], detail=False)
    def current(self, request):
        user = request.user
        user.last_login = timezone.now()
        user.save()
        serializer = self.get_serializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        refresh_token = request.data.get('refresh')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                return Response(
                    {'detail': 'Invalid token'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(status=status.HTTP_205_RESET_CONTENT)
