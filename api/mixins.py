from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class IsOwnerOrReadOnlyMixin:
    permission_classes = [IsOwnerOrReadOnly]


class IsUserOrReadOnlyMixin:
    permission_classes = [IsUserOrReadOnly]
