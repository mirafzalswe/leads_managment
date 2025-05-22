from rest_framework import serializers
from .models import Lead




class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'resume']


class LeadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'email', 'state', 'created_at', 'updated_at']

class LeadDetailSerializer(serializers.ModelSerializer):

    resume_url = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        fields = ['id', 'first_name', 'last_name', 'email', 'resume', 'resume_url', 'state', 'created_at', 'updated_at']
        read_only_fields = ['first_name', 'last_name', 'email', 'resume', 'created_at', 'updated_at']


    def get_resume_url(self, obj):
        request = self.context.get('request')
        if obj.resume and hasattr(obj.resume, 'url') and request:
            return request.build_absolute_uri(obj.resume.url)
        return None



class LeadStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['state']

    # def update(self, instance, validated_data):
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.save()
    #     return instance


