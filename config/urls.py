from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.studies.urls")),
    path("participants/", include("apps.participants.urls")),
    path("forms/", include("apps.forms.urls")),
    path("audit/", include("apps.audit.urls")),
    path("exports/", include("apps.exports.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("config.api_urls")),
]
