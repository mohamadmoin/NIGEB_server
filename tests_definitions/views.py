from rest_framework import viewsets, permissions
from .models import TestInfo, FavoriteTestGroup
from .serializers import TestInfoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import FavoriteTestGroupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class TestInfoViewSet(viewsets.ModelViewSet):
    queryset = TestInfo.objects.all()
    serializer_class = TestInfoSerializer
    permission_classes = [AllowAny]  # Add this line to require authentication
    pagination_class = None
    
    
    @action(detail=False, methods=['get'], url_path='groups')
    def get_groups(self, request):
        groups = (
            TestInfo.objects.exclude(group__exact='')
            .values_list('group', flat=True)
            .distinct()
        )
        unique_groups = list(set(groups))  # Ensure uniqueness
        unique_groups.sort()  # Optional: sort the list
        return Response(unique_groups, status=status.HTTP_200_OK)



class FavoriteTestGroupViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteTestGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


    def get_queryset(self):
        return FavoriteTestGroup.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
