from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category, Comment, Genre,
    Review, Title, User
)


USERNAME_ERROR = 'Использовать имя me в качестве username запрещено!'
REVIEW_ERROR = 'У Вас уже есть ревью к этому произведению'
YEAR_ERROR = 'Произведение еще не вышло!'


class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(USERNAME_ERROR)
        return value


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(USERNAME_ERROR)
        return value


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleWriteSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = '__all__',

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError(YEAR_ERROR)
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(
        max_value=10,
        min_value=1,
        required=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            user = self.context['request'].user
            if Review.objects.filter(
                author=user, title=title
            ).exists():
                raise serializers.ValidationError(REVIEW_ERROR)
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'review', 'author', 'pub_date')
        model = Comment
