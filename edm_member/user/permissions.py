from rest_framework import permissions

ALLOWED_IP_ADDRESS = ['20.39.197.85','127.0.0.1']


class IPBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
            
        return ip_address in ALLOWED_IP_ADDRESS
            
    def has_object_permission(self, request, view, obj):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
            
        return ip_address in ALLOWED_IP_ADDRESS