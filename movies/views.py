from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from movies.models import *
from movies.permissions import IsAuthorPermission
from movies.serializers import *


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission,]
        else:
            permissions = []
        return [permission() for permission in permissions]


class GenreViewSet(PermissionMixin, ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ActorViewSet(PermissionMixin, ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ReviewViewSet(PermissionMixin, ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RatingViewSet(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
