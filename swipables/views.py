from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin

from groups.models import GroupFoodScore

from .models import Swipe
from .serializers import SwipeSerializer


class SwipeViewset(CreateModelMixin, viewsets.GenericViewSet):
    queryset = Swipe.objects.all()
    serializer_class = SwipeSerializer

    def perform_create(self, serializer):
        instance = serializer.save(owner_username=self.request.user)

        group_food_score, created = GroupFoodScore.objects.get_or_create(
            group=instance.group,
            swipable=instance.swipable,
            session=instance.group.num_sessions,
            defaults={'score': instance.score},
        )
        if not created:
            group_food_score.score += instance.score
            group_food_score.save()
