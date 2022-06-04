from django.urls import include, path
from rest_framework import routers

from ads import views


router_ad = routers.SimpleRouter()
router_ad.register('ad', views.AdViewSet)
router_comment = routers.SimpleRouter()
router_ad.register('comment', views.CommentViewSet)

urlpatterns =  router_ad.urls + router_comment.urls