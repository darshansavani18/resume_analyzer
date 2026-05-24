from rest_framework import serializers
from .models import Resume
class ResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    class Meta:
        model =Resume
        fields = ['id', 'file', 'uploaded_at']