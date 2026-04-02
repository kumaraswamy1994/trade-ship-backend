from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Role missing in token")
        return {"role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    def __call__(self, user=Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user["role"]
