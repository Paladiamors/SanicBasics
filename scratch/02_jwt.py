import jwt

from settingsManager import get_settings


def test_read_write_token():
    settings = get_settings()
    algorithm = "HS256"
    secret = settings.get_setting("sanic/config/SANIC_JWT_SECRET")

    encoded = jwt.encode({"foo": "bar"}, secret, algorithm=algorithm)
    print(jwt.decode(encoded, secret, algorithms=[algorithm]))


def test_no_verify_token():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdFVzZXIiLCJleHAiOjE2NDQwNTMzNTMsImZvbyI6ImJhciJ9"
    sig = "yJTHxEujYwMAvt_34rQjD-kUQTICbXCd8T83e-JGIxE"

    full_token = f"{token}.{sig}"
    print(jwt.decode(full_token, options={"verify_signature": False}))
