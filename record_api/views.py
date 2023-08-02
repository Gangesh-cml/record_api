from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import record
from .serializers import recordSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class RecordListCreateView(generics.ListCreateAPIView):
    serializer_class = recordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return record.objects.filter(user=self.request.user)


class RecordRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = record.objects.all()
    serializer_class = recordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
