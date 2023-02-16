from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "amount", "payment_date", "user")

    def get_count(self):
        request = self.context.get("request")
        user_id = request.user.id

        return user_id

    def validate(self, attrs):
        user = attrs["user"]
        request_user = self.get_count()

        if user.id != request_user:
            raise serializers.ValidationError(
                "You can not create payments for another users"
            )
        return attrs


class PaymentDetailSerializer(serializers.ModelSerializer):
    user = UserIdSerializer(read_only=True, many=False)

    class Meta:
        model = Payment
        fields = (
            "id",
            "amount",
            "payment_date",
            "user",
        )
