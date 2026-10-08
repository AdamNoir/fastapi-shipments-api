from datetime import datetime, timedelta, timezone
from app.config import security_settings
import jwt

def generate_access_token(data: dict, expiry: timedelta = timedelta(days=1)):
    return jwt.encode(
            payload={
                **data,
                "exp": datetime.now(timezone.utc) + expiry
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET
        )


def decode_access_token(token: str):
    if not token or not isinstance(token, str):
        return None

    token = token.strip().strip(",")

    if "Bearer" in token:
        token = token.replace("Bearer", "").strip().strip(",")

    if "," in token:
        token = token.split(",")[0].strip()

    try: 
        return jwt.decode(
            jwt=token,
            algorithms=[security_settings.JWT_ALGORITHM],
            key=security_settings.JWT_SECRET
        )
    
    except jwt.PyJWTError:
        return None

    