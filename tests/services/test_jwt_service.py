import datetime

import jwt
import pytest

from sanaap.services import JWTService


def test_encode_generates_jwt_with_expected_subject_claim(jwt_service: JWTService):
    token = jwt_service.encode(sub="user123", ttl=datetime.timedelta(hours=1))
    assert isinstance(token, str)
    assert token

    # Decode using PyJWT directly to verify the raw token contents,
    # independent of JWTService.decode() implementation.
    claims = jwt.decode(
        token,
        key=jwt_service._secret_key,
        algorithms=[jwt_service._algorithm],
    )

    assert claims["sub"] == "user123"


def test_decode_returns_subject_for_valid_token(jwt_service: JWTService):
    token = jwt_service.encode(sub="user123", ttl=datetime.timedelta(hours=1))
    sub = jwt_service.decode(token)
    assert sub == "user123"


def test_decode_raises_value_error_for_malformed_token(jwt_service: JWTService):
    with pytest.raises(ValueError):
        jwt_service.decode("invalid.token.here")


def test_decode_raises_value_error_for_expired_token(jwt_service: JWTService):
    token = jwt_service.encode(sub="user123", ttl=datetime.timedelta(seconds=-1))
    with pytest.raises(ValueError):
        jwt_service.decode(token)
