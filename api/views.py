# collab/views.py
from rest_framework import viewsets
from django.db.models import Q
from .models import Project, Task, AuditLog
from .serializers import ProjectSerializer, TaskSerializer, AuditLogSerializer
from .permissions import PermitPermission
from django.utils import timezone

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [PermitPermission]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [PermitPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(access_expires__isnull=True) | Q(access_expires__gt=timezone.now())
            )
        return queryset

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [PermitPermission]

    def get_queryset(self):
        # Extra safety: Restrict to admins if Permit.io fails
        if not self.request.user.is_staff:
            return AuditLog.objects.none()
        return AuditLog.objects.all()