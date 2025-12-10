import jwt
import datetime

secret = "Booooooooooooooooom"
def create_token(payload):
    return (jwt.encode(payload, secret, algorithm="HS256"))

def decode_token(token):
    payload = jwt.decode(token, secret, algorithms= "HS256")
    return(payload)

