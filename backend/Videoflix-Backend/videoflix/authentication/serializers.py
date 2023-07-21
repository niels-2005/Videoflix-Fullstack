from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class RegisterUserSerializer(serializers.ModelSerializer):
    password_again = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "password_again"]

    def validate(self, data):
        if data["password"] != data["password_again"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def create(self, validated_data):
        validated_data.pop("password_again")
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        confirmation_token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        return {"user": user, "uid": uid, "token": confirmation_token}


class EmailConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        for user in get_user_model().objects.filter(is_active=False):
            if default_token_generator.check_token(user, value):
                user.is_active = True
                user.save()
                return value
        raise serializers.ValidationError("Invalid token.")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = get_user_model().objects.filter(email=data["email"]).first()
        if user:
            if user.is_active:
                auth_user = authenticate(
                    username=user.username, password=data["password"]
                )
                if auth_user:
                    token, created = Token.objects.get_or_create(user=auth_user)
                    return {"token": token.key, "username": auth_user.username}
                else:
                    raise serializers.ValidationError("Invalid email or password.")
            else:
                raise serializers.ValidationError("Please confirm your E-Mail.")
        else:
            raise serializers.ValidationError("Invalid email or password.")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = get_user_model().objects.get(email=value)
            return value
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = get_user_model().objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return {"uid": uid, "token": token}


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_uid(self, value):
        try:
            uid = force_text(urlsafe_base64_decode(value))
            user = get_user_model().objects.get(pk=uid)
            return value
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError("Invalid uid.")
        return value

    def save(self):
        uid = force_text(urlsafe_base64_decode(self.validated_data["uid"]))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, self.validated_data["token"]):
            user.set_password(self.validated_data["password1"])
            user.save()
            return {"detail": "Password reset successful."}
        else:
            raise serializers.ValidationError("Invalid token.")
