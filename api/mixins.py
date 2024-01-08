from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class IsOwnerOrReadOnlyMixin:
    permission_classes = [IsOwnerOrReadOnly]
