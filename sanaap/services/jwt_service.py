import datetime

import jwt


class JWTService:
    """JWT-based token service for encoding and decoding tokens."""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """Initialize the JwtTokenService with configuration parameters."""
        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, sub: str, ttl: datetime.timedelta) -> str:
        """Encode a new token for the given subject"""
        now = datetime.datetime.now(datetime.UTC)
        exp = now + ttl
        claims = {"sub": sub, "iss": now.timestamp(), "exp": exp.timestamp()}
        return jwt.encode(payload=claims, key=self._secret_key, algorithm=self._algorithm)

    def decode(self, raw_token: str) -> str:
        """Decode and validate the given token and returns the sub"""
        try:
            claims = jwt.decode(
                jwt=raw_token,
                key=self._secret_key,
                algorithms=[self._algorithm],
            )
        except (jwt.PyJWTError, ValueError) as e:
            raise ValueError from e

        return claims["sub"]
