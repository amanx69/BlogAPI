from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

def get_token(user):
    """Generate JWT access + refresh token pair for a user."""
    if not user.is_active:
        raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }