from rest_framework import serializers
from reviews.models import Review, Comment
from django.shortcuts import get_object_or_404

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        ref_name = 'ReadOnlyUsers'

class SendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        max_length=150, required=True, regex=r"^[\w.@+-]+\Z"
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Некорректный username = "{value}"'
            )
        return value


class SendTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150, required=True, regex=r"^[\w.@+-]+\Z"
    )
    confirmation_code = serializers.CharField(required=True)


class UpdateSelfSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=False)
    username = serializers.RegexField(
        max_length=150, required=False, regex=r"^[\w.@+-]+\Z"
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'pub_date', 'score')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
        