from rest_framework import permissions

class BasePermission(object):
    """
    All permissions should come from here
    """

    def has_permission(self, request, view):
        """
        If permision is granted return True
        """
        return True
    

# Overide built in permisions (has_object_permission)
class IsAuthorOrReadOnly():
    
    def has_object_permission(self, request, view, obj):
        """
        Read only for any request
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Writes are allowed for only the author of the article
        return obj.author == request.user
    
    def has_permission(self, request, obj):
        return True