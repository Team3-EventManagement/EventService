from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
from . import schemas

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. "
        "It must match the SECRET_KEY used by UserService to sign JWTs."
    )
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# HTTPBearer reads the token from the Authorization: Bearer <token> header.
# This service does NOT issue tokens — it only validates tokens signed by UserService.
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # We assume the UserService includes 'user_id' and 'sub' (username) in the JWT payload
        user_id = payload.get("user_id")
        username = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = schemas.TokenData(user_id=user_id, username=username)
    except JWTError:
        raise credentials_exception
        
    return token_data
