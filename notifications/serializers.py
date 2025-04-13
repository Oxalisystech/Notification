from rest_framework import serializers



class BaseNotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    user = serializers.IntegerField(source='user_id')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        excluded_fields = kwargs.pop('excluded_fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if excluded_fields is not None:
            all_fields = set(self.fields.keys())
            disallowed = set(excluded_fields)
            for field_name in all_fields.intersection(disallowed):
                self.fields.pop(field_name)

    class Meta:
        model = None  # You need to set this in the derived serializers
        fields = ['title', 'description', 'level', 'user', 'created_at', 'read_at']

    @staticmethod
    def get_created_at(obj):
        try:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as err:
            return str(err)

    @staticmethod
    def get_modified_at(obj):
        try:
            return obj.modified_at.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as err:
            return str(err)






