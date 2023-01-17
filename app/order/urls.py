"""
URL mappings for the Order APIs.
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from order import views

router = DefaultRouter()
router.register('orders', views.OrderViewset)

app_name = 'order'

urlpatterns = [
    path('', include(router.urls)),
]
