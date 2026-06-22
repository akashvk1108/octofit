from rest_framework import serializers


class ActivitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(max_length=150)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    duration_minutes = serializers.IntegerField(min_value=0)
    date = serializers.DateField()
