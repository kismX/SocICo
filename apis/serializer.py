from accounts.models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'age', 'gender', 'location', 'bio', 'interests', 'last_online', 'invisible']