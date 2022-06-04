from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated

class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_serializer_class(self):
        if self.action in ["retrieve","create", "update", "partial_update", "destroy"]:
            return  AdDetailSerializer
        return AdSerializer

    def get_permissions(self):
        permission_classes = (AllowAny,)
        if self.action == "create":
            permission_classes = (IsAuthenticated,)
        if self.action in ["update", "partial_update", "destroy", "me"]:
            permission_classes = (IsOwner | IsAdmin, )
        return tuple(permission() for permission in permission_classes)

    def get_queryset(self):
        if self.action == "me":
            return Ad.objects.filter(user=self.request.user).all()
        return Ad.objects.all()

    @action(
        detail=False,
        methods=["get",],
    )
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        permission_classes = (AllowAny,)
        if self.action == "create":
            permission_classes = (IsAuthenticated,)
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = (IsOwner | IsAdmin, )
        return tuple(permission() for permission in permission_classes)

