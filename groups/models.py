from django.db import models

from common.models import TimeStampedModel


class Group(TimeStampedModel):
    owner_username = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, related_name='user_groups')
    name = models.CharField(max_length=100)
    composite_key = models.CharField(
        max_length=200, primary_key=True)
    members = models.ManyToManyField(
        'users.User', related_name='group_members', blank=True)
    capacity = models.IntegerField(default=10)
    num_sessions = models.IntegerField(default=0)

    @property
    def member_count(self):
        return self.members.count()

    def save(self, *args, **kwargs):
        if self.name != self.owner_username.username:
            self.composite_key = f'{self.owner_username.username}_{self.name}'
        else:
            self.composite_key = self.name
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner_username.username} - {self.name}"

    class Meta:
        ordering = ['created']
        unique_together = ['owner_username', 'name']


class SendGroupInvite(TimeStampedModel):
    sending_username = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='sending_group_invites')
    group = models.ForeignKey(
        'groups.Group', on_delete=models.CASCADE, related_name='group_invites')
    receiving_username = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='receiving_group_invites')
    accepted = models.BooleanField(blank=True, null=True)
    composite_key = models.CharField(
        max_length=400, primary_key=True)

    def save(self, *args, **kwargs):
        self.composite_key = (
            f'{self.sending_username.username}_{self.group.composite_key}_{self.receiving_username.username}'
        )
        super(SendGroupInvite, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.sending_username.username} - {self.group.composite_key} - {self.receiving_username.username}"

    class Meta:
        ordering = ['created']
        unique_together = ['sending_username', 'group', 'receiving_username']


class GroupFoodScore(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    swipable = models.ForeignKey(
        'swipables.Swipable',
        on_delete=models.CASCADE,
        related_name='group_food_scores'
    )
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='group_food_scores'
    )
    score = models.IntegerField()
    session = models.IntegerField()

    def __str__(self):
        return f"{self.swipable} - {self.group} - {self.session}"

    class Meta:
        ordering = ['created']
        unique_together = ['swipable', 'group', 'session']
