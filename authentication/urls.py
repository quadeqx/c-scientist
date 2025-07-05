from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title='Authentication API',
        default_version='v1',
        description='Authentication backend API',
        terms_of_service='',
        contact=openapi.Contact(email=''),
        license=openapi.License(name=''),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user', include('auths.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='swagger-schema'
    ),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0),
        name='redoc-schema'
    ),



]



