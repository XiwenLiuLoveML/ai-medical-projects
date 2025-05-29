# rbac.py
# -----------------------------------------
# 📁 Description:
# This module implements Role-Based Access Control (RBAC) as a FastAPI dependency.
# It validates JWT scopes, staff status, and basic user role requirements.
#
# Note: Simplified for public demo purposes.
# -----------------------------------------

from fastapi import Depends, Request

from common.exception.errors import AuthorizationError, TokenError
from common.security.jwt import DependsJwtAuth


class RBAC:
    async def rbac_verify(self, request: Request, _token: str = DependsJwtAuth) -> None:
        path = request.url.path

        # Ensure token has proper scopes
        if not request.auth.scopes:
            raise TokenError

        # Allow superusers to bypass
        if request.user.is_superuser:
            return

        # User must have at least one role
        if not request.user.roles:
            raise AuthorizationError(msg='User has no assigned roles')

        # POST/PUT/DELETE requires staff permission
        if request.method not in ['GET', 'OPTIONS']:
            if not request.user.is_staff:
                raise AuthorizationError(msg='User not authorized for admin operations')


rbac = RBAC()
DependsRBAC = Depends(rbac.rbac_verify)
