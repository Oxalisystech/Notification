from django.conf import settings

class UserNotificationManager:
    def __init__(self, id):
        self.user_id = id
        self.notification_limit = getattr(settings, 'NOTIFICATION_PAGE_SIZE', 10)

    @staticmethod
    def get_notification_models():
        from notifications.models import BaseNotification
        return {model.name(): model for model in BaseNotification.get_all_subclasses()}

    def get_categories_unread_count(self):
        notifications = self.get_notifications()
        return {notification_category: notification_queryset.filter(read_at_isnull=True).count() for
                notification_category, notification_queryset in notifications.items()}

    def get_notification_categories(self):
        return list(self.get_notification_models().keys())

    def get_notifications(self):
        data = {}
        for model in self.get_notification_models().values():
            queryset = model.objects.filter(user_id=self.user_id)[:self.notification_limit]
            data[model.name()] = queryset
        return data

    def get_serialized_notifications(self):
        user_notifications = self.get_notifications()
        serialized_notifications = {
            notification_category: notification_queryset.model.serializer_class()(
                notification_queryset,
                many=True,
                context={'unread_queryset': notification_queryset.filter(read_at_isnull=True)}).data
            for notification_category, notification_queryset in user_notifications.items()}
        return serialized_notifications

    def get_notification(self, model):
        return model.objects.filter(user=self.user_id)

    def get_serialized_notification(self, model):
        notifications = self.get_notification(model)
        return model.serializer_class()(notifications, many=True,
                                        context={'unread_queryset': notifications.filter(read_at_isnull=True)}).data