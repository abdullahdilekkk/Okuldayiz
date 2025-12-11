from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name = "schema"), name = "swagger-ui"),

    path("api/token/", TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name = "toke_refresh"),

    path('admin/', admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/schools/", include("schools.urls")),
    path("api/leads/", include("leads.urls"))
]
