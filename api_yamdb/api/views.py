from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import (permissions, viewsets, status, filters, mixins)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User, Review
from .permissions import (IsAdminOrSuperUser, IsAdminOrReadOnly,
                          IsAdminOrModeratorOrAuthor,)
from .pagination import TitlePagination
from .serializers import (
    CategorySerializer, GenreSerializer, SignUpSerializer,
    TitleWriteSerializer, TitleReadSerializer, TokenSerializer, UserSerializer,
    CommentSerializer, ReviewSerializer
)
from .send_code import send_code
from .filtersets import TitleFilter

SINGUP_ERROR = 'данный {key} уже занят'
CODE_ERROR = 'Неверный confirmation_code'


class APISignup(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user, created = User.objects.get_or_create(**data)
        except Exception as mistake:
            if User.objects.filter(username=data['username']).exists():
                return Response(
                    {'email': SINGUP_ERROR.format(key='email'),
                     'error': str(mistake)},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'username': SINGUP_ERROR.format(key='username'),
                 'error': str(mistake)},
                status=status.HTTP_400_BAD_REQUEST)
        code = default_token_generator.make_token(user=user)
        send_code(user.email, code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(
            User,
            username=data.get('username')
        )
        if default_token_generator.check_token(
                user, data.get('confirmation_code')) is False:
            return Response(
                {'confirmation_code': CODE_ERROR},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user=user)
        return Response(
            {
                'token': str(refresh.access_token)
            }
        )


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user, data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, patrial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    pagination_class = TitlePagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleReadSerializer
        return TitleWriteSerializer


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrModeratorOrAuthor,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrModeratorOrAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )
