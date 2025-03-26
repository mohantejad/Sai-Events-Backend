import logging
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)  # Get from cookies
            else:
                raw_token = self.get_raw_token(header)  # Get from Authorization header
            
            if raw_token is None:
                return None  # No token provided, allow unauthenticated access where applicable

            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        
        except AuthenticationFailed as e:  # Handle JWT validation errors
            logger.warning(f"Authentication failed: {str(e)}")  # Log error for debugging
            return None  # Do not block unauthenticated users
