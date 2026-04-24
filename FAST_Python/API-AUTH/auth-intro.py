from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# --------------------------------------------------
# ⚙️ SETTINGS (modern via ENV möglich)
# --------------------------------------------------

class Settings(BaseSettings):
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()

# --------------------------------------------------
# 🚀 APP
# --------------------------------------------------

app = FastAPI(
    title="Modern FastAPI Auth",
    description="JWT Auth mit aktuellen Python-Tools (uv, pydantic-settings)",
    version="2.0"
)

# --------------------------------------------------
# 🔐 SECURITY SETUP
# --------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    description="JWT Token hier einfügen (Bearer <token>)"
)

# --------------------------------------------------
# 👤 MODELS
# --------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

# --------------------------------------------------
# 🗄️ FAKE DB
# --------------------------------------------------

fake_users_db = {
    "marcus": {
        "username": "marcus",
        "hashed_password": pwd_context.hash("secret"),
    }
}

# --------------------------------------------------
# 🔧 HELPERS
# --------------------------------------------------

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_user(username: str):
    return fake_users_db.get(username)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# --------------------------------------------------
# 🔑 AUTH ROUTES
# --------------------------------------------------

@app.post(
    "/auth/login",
    response_model=Token,
    summary="Login und JWT erhalten",
    tags=["Auth"]
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    token = create_access_token({"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# --------------------------------------------------
# 🔒 PROTECTED
# --------------------------------------------------

@app.get(
    "/users/me",
    summary="Aktueller Benutzer",
    tags=["User"]
)
def read_me(user: dict = Depends(get_current_user)):
    return {"username": user["username"]}

# --------------------------------------------------
# 🌍 PUBLIC
# --------------------------------------------------

@app.get(
    "/health",
    summary="Health Check",
    tags=["Public"]
)
def health():
    return {"status": "ok"}