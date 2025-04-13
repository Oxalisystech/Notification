from django.db import models
from django.utils  import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .managers import SoftDeleteManager




class BaseNotification(models.Model):
    class NotificationLevel(models.IntegerChoices):
        low = 1,
        medium = 2,
        high = 3

    user_id = models.IntegerField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True, default=None)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    level = models.IntegerField(choices=NotificationLevel.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    objects = SoftDeleteManager()

    @classmethod
    def get_all_subclasses(cls):
        subclasses = cls.__subclasses__()
        all_subclasses = subclasses.copy()
        for subclass in subclasses:
            all_subclasses.extend(subclass.get_all_subclasses())
        return all_subclasses

    @classmethod
    def create_notifications(cls, title: str, description: str, level: int, users: list[int], type=None):
        try:
            for user_id in users:
                cls.objects.create(title=title, description=description, level=level,
                                   user=user_id) if not type else cls.objects.create(
                    title=title, description=description, level=level, user=user_id, type=type
                )
        except Exception as err:
            return str(err)

    def dispatch(self):
        serializer = self.__class__.serializer_class()(self, excluded_fields=['user'])

        channel_layer = get_channel_layer()
        channel_name = self.get_channel_name()
        async_to_sync(channel_layer.group_send)(
            channel_name,  # This should match the group your WebSocket consumer is listening to
            {
                'type': 'notifications',  # This should match the method name in your WebSocket consumer
                'message': 'New Notification',
                'action': self.__class__.__name__,
                'payload': {
                    'notification': serializer.data
                }
            }
        )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print("BEFORE SAVE")
        try:
            super(BaseNotification, self).save(*args, **kwargs)
        except Exception as err:
            print(err)
        print("SAVED")
        self.dispatch()

    def get_channel_name(self):
        return f"user_{self.user_id}"

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"user_id:{self.user_id}, title:{self.title}"