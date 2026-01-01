from typing import Annotated
from fastapi import APIRouter, Header

router = APIRouter(prefix="/api/debug", tags=["debug"])

@router.get("/check-token")
async def check_token(
    authorization: Annotated[str | None, Header()] = None
):
    """
    Debug endpoint to inspect the authorization token
    """
    if not authorization:
        return {
            "error": "No authorization header provided",
            "authorization": None
        }

    parts = authorization.split()

    return {
        "full_header": authorization,
        "parts_count": len(parts),
        "parts": parts,
        "token": parts[1] if len(parts) > 1 else None,
        "token_length": len(parts[1]) if len(parts) > 1 else 0,
        "token_segments": len(parts[1].split('.')) if len(parts) > 1 else 0,
    }
