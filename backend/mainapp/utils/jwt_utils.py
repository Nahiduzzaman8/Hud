import jwt
import datetime
secret = "Booooooooooooooooom"
def create_token(payload):
    return (jwt.encode(payload, secret, algorithm="HS256"))

