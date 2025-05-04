from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin

from groups.models import Group, GroupFoodScore

from .models import Swipable, Swipe
from .serializers import SwipableListSerializer, SwipeSerializer


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


class SwipableListView(ListAPIView):
    serializer_class = SwipableListSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        if not group_id:
            raise ValidationError(
                {"detail": "group parameter is required as a query parameter."})

        session = get_object_or_404(Group, pk=group_id).num_sessions
        swiped_swipables = Swipe.objects.filter(
            owner_username=self.request.user, group_id=group_id, session=session
        ).values_list('swipable_id', flat=True)

        return Swipable.objects.exclude(id__in=swiped_swipables)
