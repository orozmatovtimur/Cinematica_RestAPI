from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from movies.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="IMDB clone API",
      default_version='v1',
      description="There is API for movie database !",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register('movie', MovieViewSet)
router.register('actor', ActorViewSet)
router.register('review', ReviewViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui()),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
