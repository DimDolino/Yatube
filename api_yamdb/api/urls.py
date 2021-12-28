from django.urls import path, include
from rest_framework import routers

from .views import (
    APISignup, APIToken, CategoryViewSet, GenreViewSet,
    TitleViewSet, UserViewSet, CommentViewSet, ReviewViewSet)

REVIEW_URL = r'titles/(?P<title_id>\d+)/reviews'
COMMENT_URL = REVIEW_URL + r'/(?P<review_id>[\d]+)/comments'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register(REVIEW_URL, ReviewViewSet, basename='review')
router_v1.register(COMMENT_URL, CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
]
