import time
import secrets
from .models import Security
from pydantic.dataclasses import dataclass
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status
from . import smc_db_aio

MOCK_USER = {
    "hsa18ms082": "1234",
    "raj": "abc",
}

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def validate_user(username: str, password: str):
    # TODO ldap
    real_pass = MOCK_USER.get(username)
    if (real_pass is not None) and (password == real_pass):
        return True
    return False


def generate_token():
    # first 10 digits time inseconds, then random token 9 char
    # TODO read uuid
    return str(int(time.time())) + secrets.token_urlsafe(5);


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # user = fake_decode_token(token)
    sec = await Security.filter(token=token).first()
    if sec is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return sec.uid

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    # validate user
    if not await validate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    uid, balance = await smc_db_aio.get_user_details('hsa18ms082@iiserkol.ac.in')

    sec = await Security.create(
            token=generate_token(),
            uid=uid
        )
    return {"access_token": sec.token, "token_type": "bearer"}


@router.get("/logout")
async def logout(token = Depends(oauth2_scheme)) -> dict:
    it = await Security.filter(token=token).first()
    if it:
        print("deleting it")
        await it.delete()
    return {"success": "Logged out"}
