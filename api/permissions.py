from permit import Permit
from rest_framework import permissions
from django.conf import settings

class PermitPermission(permissions.BasePermission):
    def __init__(self):
        print(f"Initializing Permit with PERMIT_API_KEY: {settings.PERMIT_API_KEY}")
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
            return False

        resource = view.basename  # e.g., 'project'
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
        user_key = str(user.id)  # User ID as a string
        resource_obj = {
            "type": resource,  # e.g., "project"
            "attributes": resource_attributes if resource_attributes else None
        }

        try:
            allowed = self.permit.check(
                user=user_key,  # User ID as a string
                action=action,  # e.g., "read"
                resource=resource_obj  # Resource as a dict
            )
            print(f"Permit.check result for user {user_key}, action {action}, resource {resource}: {allowed}")
        except Exception as e:
            print(f"Permit.check failed: {str(e)}")
            return False

        if allowed:
            from .models import AuditLog
            AuditLog.objects.create(
                user=user,
                action=f"{resource}_{action}",
                resource=resource
            )
        return allowed