from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

app_name = 'core'

router = DefaultRouter()
router.register('api/v1/categories', views.CategoryViewset)
router.register('api/v1/products', views.ProductViewset)


urlpatterns = [
    path('', include(router.urls))
]