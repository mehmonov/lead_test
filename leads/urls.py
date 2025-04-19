from django.urls import include, path
from rest_framework.routers import DefaultRouter

from leads.views import LeadViewSet

router = DefaultRouter()
router.register("", LeadViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
