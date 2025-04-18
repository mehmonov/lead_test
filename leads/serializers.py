from rest_framework import serializers
from .models import Lead

ALLOWED_FILE_TYPES = ['application/pdf']
MAX_FILE_SIZE_MB = 5

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'resume',
            'state',
            'submitted_at',
        ]
        read_only_fields = ['id', 'state', 'submitted_at']

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value

    def validate_email(self, value):
        if Lead.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email has already submitted a lead.")
        return value

    def validate_resume(self, file):
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise serializers.ValidationError("Resume must be a PDF or Word document.")
        if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError("Resume file size must be under 5MB.")
        return file
