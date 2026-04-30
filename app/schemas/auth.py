# app/schemas/auth.py
import re
from datetime import date

from pydantic import BaseModel, validator


PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$")
PASSWORD_REQUIREMENT = (
    "Password must contain at least one capital letter, one number, "
    "and one special symbol"
)


class NonEmptyStringModel(BaseModel):
    @validator("*", pre=True)
    def strip_strings(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty")

        return value


class CivilianAddressCreate(NonEmptyStringModel):
    zip_code: str
    state: str
    city: str
    street: str
    house: str


class CivilianRegisterRequest(NonEmptyStringModel):
    address: CivilianAddressCreate
    email: str
    username: str
    password: str
    phone_number: str
    licence_number: str
    state_issue: str
    last_name: str
    first_name: str
    dob: date
    height_inches: int
    weight_pounds: int
    eyes_colour: str

    @validator("password")
    def password_meets_requirements(cls, value):
        if not PASSWORD_PATTERN.match(value):
            raise ValueError(PASSWORD_REQUIREMENT)

        return value

    @validator("email")
    def email_is_valid(cls, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Email must be valid")

        return value

    @validator("height_inches")
    def height_is_realistic(cls, value):
        if value < 36 or value > 96:
            raise ValueError("Height must be between 36 and 96 inches")

        return value

    @validator("weight_pounds")
    def weight_is_realistic(cls, value):
        if value < 50 or value > 500:
            raise ValueError("Weight must be between 50 and 500 pounds")

        return value


class CivilianResponse(BaseModel):
    driver_id: int
    email: str
    username: str
    phone_number: str
    licence_number: str
    state_issue: str
    last_name: str
    first_name: str
    dob: date
    height_inches: int
    weight_pounds: int
    eyes_colour: str


class CivilianContactUpdateRequest(NonEmptyStringModel):
    email: str
    phone_number: str

    @validator("email")
    def email_is_valid(cls, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Email must be valid")

        return value


class LoginRequest(NonEmptyStringModel):
    username: str
    password: str


class AdminLoginRequest(LoginRequest):
    badge_number: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str


class CivilianTokenResponse(TokenResponse):
    driver_id: int


class AdminTokenResponse(TokenResponse):
    badge_number: str
    username: str
    first_name: str
    last_name: str
