from rest_framework import serializers

from apps.news.models import News


class NewsSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(child=serializers.FileField(), required=False, default=[])

    class Meta:
        model = News
        fields = '__all__'