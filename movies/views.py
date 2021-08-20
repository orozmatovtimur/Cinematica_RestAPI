from django.db.models import Q
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from movies.permissions import IsAuthorPermission
from movies.serializers import *
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


# class PermissionMixin:
#     def get_permissions(self):
#         if self.action == 'create':
#             permissions = [IsAuthenticated,]
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             permissions = [IsAuthorPermission,]
#         else:
#             permissions = []
#         return [permission() for permission in permissions]


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        for i in permissions:
            print(i())
        return [permission() for permission in permissions]


class GenreViewSet(PermissionMixin, ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(PermissionMixin, ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    #TODO: search не проверял
    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        queryset = super().get_queryset()
        score_count = int(self.request.query_params.get('imdb_score', 0))
        if score_count > 0:
            queryset = queryset.filter(imdb_score__gte=score_count)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_filter = self.request.query_params.get('genre', '')
        if genre_filter == self.request.query_params.get('genre'):
            queryset = queryset.filter(genre=genre_filter)
        return queryset


class ActorViewSet(PermissionMixin, ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RatingViewSet(ModelViewSet):  # PermissionMixin
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['get'])
    def favourites(self, request, pk=None):
        queryset = self.get_queryset()
        likes = queryset.filter(user=request.user)
        movie_list = [like.movie for like in likes]
        serializer = MovieSerializer(movie_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




