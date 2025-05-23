from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import Lead




class LeadCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[EmailValidator()],
        help_text="Valid email address of the lead"
    )
    first_name = serializers.CharField(
        max_length=20,
        help_text="First name of the lead"
    )
    last_name = serializers.CharField(
        max_length=20,
        help_text="Last name of the lead"
    )
    resume = serializers.FileField(
        required=False,
        help_text="Resume file (PDF, DOC, or DOCX format, max 5MB)"
    )

    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'resume']

    def validate(self, data):
        """
        Validate the entire data set.
        """
        # Add any cross-field validation here
        return data


class LeadListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ['id', 'full_name', 'email', 'state', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LeadDetailSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 
                 'resume', 'resume_url', 'state', 'created_at', 'updated_at']
        read_only_fields = ['first_name', 'last_name', 'email', 'resume', 
                           'created_at', 'updated_at']

    def get_resume_url(self, obj):
        request = self.context.get('request')
        if obj.resume and hasattr(obj.resume, 'url') and request:
            return request.build_absolute_uri(obj.resume.url)
        return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"



class LeadStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['state']

    def validate_state(self, value):
        """
        Validate that the state is one of the allowed choices.
        """
        if value not in dict(Lead.LeadState.choices):
            raise serializers.ValidationError(
                f"Invalid state. Must be one of: {', '.join(dict(Lead.LeadState.choices).keys())}"
            )
        return value


