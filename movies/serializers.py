from decimal import Decimal

from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    # genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        print(action)
        if action == 'list' or action == 'retrieve':
            if action == 'list':
                representation['reviews'] = instance.reviews.count()
            else:
                representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data

            rates = Rating.objects.filter(movie=instance)
            if not rates:
                representation['rating'] = 'null'
            else:
                sum = 0
                for i in rates:
                    sum = sum + i.value
                representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(movie=instance).count())

        return representation


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("user", "value", "movie")

