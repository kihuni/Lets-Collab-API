from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'audit_logs', AuditLogViewSet, basename='audit_logs')

urlpatterns = [
    path('', include(router.urls)),
]