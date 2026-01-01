from typing import Annotated
from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session
from app.core.security import validate_session_token
from app.core.database import get_session

def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(get_session)
) -> str:
    """
    FastAPI dependency for extracting authenticated user ID from Better Auth session token.

    Args:
        authorization: Authorization header (Bearer <token>)
        session: Database session

    Returns:
        User ID from valid session

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    user_id = validate_session_token(token, session)

    return user_id
