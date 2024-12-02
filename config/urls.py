from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
            openapi.Info(
                # название нашей документации
                title="Snippets API for Library app",
                # версия документации
                default_version='v1',
                # описание нашей документации
                description="Документация для приложения Library app",
                terms_of_service="https://www.google.com/policies/terms/",
                contact=openapi.Contact(email="contact@snippets.local"),
                license=openapi.License(name="BSD License"),
            ),
            public=True,
            # в разрешениях можем сделать доступ только авторизованным пользователям.
            permission_classes=(permissions.AllowAny,),
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls', namespace='library')),
    path('users/', include('users.urls', namespace='users')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
