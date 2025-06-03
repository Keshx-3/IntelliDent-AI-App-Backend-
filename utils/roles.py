from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from utils.token import oauth2_scheme
from config import SECRET_KEY, ALGORITHM

def require_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin privileges required")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
