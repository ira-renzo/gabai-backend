from rest_framework import serializers

from app.models import News


class NewsSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(child=serializers.FileField(), required=False, default=[])

    class Meta:
        model = News
        fields = '__all__'