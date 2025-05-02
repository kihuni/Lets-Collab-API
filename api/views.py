from rest_framework import viewsets
from .models import Project, Task, AuditLog
from .serializers import ProjectSerializer, TaskSerializer, AuditLogSerializer
from .permissions import PermitPermission

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [PermitPermission]
    basename = 'project'

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [PermitPermission]
    basename = 'task'

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [PermitPermission]
    basename = 'audit_log'