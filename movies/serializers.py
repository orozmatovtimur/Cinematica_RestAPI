from decimal import Decimal

from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name',)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        # fields = '__all__'
        exclude = ('author',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        action = self.context.get('action')
        if action == 'list' or action == 'retrieve':
            if action == 'list':
                representation['reviews'] = instance.reviews.count()
                representation['like'] = instance.likes.count()
            else:
                representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
                representation['like'] = LikeSerializer(instance.likes.all(), many=True).data

            rates = Rating.objects.filter(movie=instance)
            if not rates:
                representation['rating'] = 'null'
            else:
                sum = 0
                for i in rates:
                    sum = sum + i.value
                representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(movie=instance).count())

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data["author_id"] = user_id
        movie = Movie.objects.create(**validated_data)
        return movie


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email

        return representation

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     validated_data["user"] = user
    #     review = Review.objects.create(**validated_data)
    #     return review


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("user", "value", "movie")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email

        return representation


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        movie = validated_data.get('movie')

        if Like.objects.filter(user=user, movie=movie):
            like = Like.objects.get(user=user, movie=movie)
            return like

        like = Like.objects.create(user=user, **validated_data)
        return like




