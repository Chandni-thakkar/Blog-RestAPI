from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Define the OpenAPI Info
schema_info = openapi.Info(
    title="Blog API",
    default_version='v1',
    description="API documentation for blog project",
    contact=openapi.Contact(email="chandnithakkar1214@gmail.com"),
    license=openapi.License(name="BSD License"),
)

# Define schema view
schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Define the security scheme for Bearer token authentication
security_scheme = openapi.Schema(
    type=openapi.TYPE_STRING,
    in_=openapi.IN_HEADER,
    name="Authorization",
    description="JWT Authorization header using the Bearer scheme. Example: `Bearer <your-token>`",
)

# Add the security definition to the schema
schema_view.security_definitions = {
    'Bearer': security_scheme
}

# Set up URL patterns
urlpatterns = [
    # Swagger JSON/YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Authentication URLs
    path('auth/', include('apps.authentication.urls')),
    # Blog API URLs
    path('api/', include('apps.blog.urls')),
]
