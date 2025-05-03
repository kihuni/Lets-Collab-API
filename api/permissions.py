# collab/permissions.py
import asyncio
from permit import Permit
from rest_framework import permissions
from django.conf import settings
from django.utils import timezone
from .models import AuditLog

class PermitPermission(permissions.BasePermission):
    def __init__(self):
        if not settings.PERMIT_API_KEY:
            raise ValueError("PERMIT_API_KEY is not set in settings. Check .env file.")
        try:
            self.permit = Permit(
                pdp="https://cloudpdp.api.permit.io",
                token=settings.PERMIT_API_KEY
            )
            print("Permit initialized successfully")
        except Exception as e:
            raise ValueError(f"Failed to initialize Permit: {str(e)}")

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            print("User not authenticated")
            return False

        # Determine resource and action
        resource = view.basename if hasattr(view, 'basename') else 'unknown'
        # Map plural basenames to singular resource names expected by Permit.io
        resource_map = {
            'projects': 'project',
            'tasks': 'task',
            'audit_logs': 'audit_log'
        }
        resource = resource_map.get(resource, resource)  # Use mapped name if available

        action = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'DELETE': 'delete'
        }.get(request.method, 'read')

        # Prepare resource attributes
        resource_attributes = {}
        if 'project_id' in request.data or 'project_id' in request.query_params:
            resource_attributes['project_id'] = request.data.get('project_id', request.query_params.get('project_id'))

        # Construct user and resource for Permit.check()
        user_key = str(user.id)
        resource_obj = {
            "type": resource,
            "attributes": resource_attributes if resource_attributes else None
        }

        # Debug logging
        print(f"Checking permission for user_id: {user_key}, action: {action}, resource: {resource}, attributes: {resource_attributes}")

        try:
            allowed = asyncio.run(
                self.permit.check(
                    user=user_key,
                    action=action,
                    resource=resource_obj
                )
            )
            print(f"Permit.check result for user {user_key}, action {action}, resource {resource}: {allowed}")
        except Exception as e:
            print(f"Permit.check failed: {str(e)}")
            return False

        if allowed:
            try:
                AuditLog.objects.create(
                    user=user,
                    action=f"{resource}_{action}",
                    resource=resource,
                    timestamp=timezone.now()
                )
            except Exception as e:
                print(f"Failed to create audit log: {str(e)}")

        return allowed