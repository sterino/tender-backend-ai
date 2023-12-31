from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from ..service import Service, get_service
from . import router


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    bin: str


class RegisterUserResponse(BaseModel):
    email: str


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
):
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )
    gosuser = svc.repository.get_user_by_bin(input.bin)
    if gosuser is not None:
        print(
            gosuser,
        )
        svc.repository.create_user(input.dict(), gosuser)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bin is not defined.",
        )

    return RegisterUserResponse(email=input.email)
