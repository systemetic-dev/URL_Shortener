from rest_framework import serializers
from apps.shortener.models import URL
from django.contrib.auth.models import User

class ShortenURLSerializer(serializers.ModelSerializer):

    custom_code = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = URL
        fields = ["original_url", "custom_code"]

    def validate_custom_code(self, value):

        if not value:
            return value

        # length validation
        if len(value) < 3:
            raise serializers.ValidationError("Code too short")

        # uniqueness check
        if URL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("Code already exists")

        return value

    def create(self, validated_data):

        custom_code = validated_data.pop("custom_code", None)

        url = URL(**validated_data)

        if custom_code:
            url.short_code = custom_code
            url.save()
        else:
            url.save()  # triggers auto-generation

        return url
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])  # 🔐 hashing
        user.save()
        return user
    
class URLListSerializer(serializers.ModelSerializer):

    class Meta:
        model = URL
        fields = [
            "id",
            "original_url",
            "short_code",
            "click_count",
            "created_at",
        ]