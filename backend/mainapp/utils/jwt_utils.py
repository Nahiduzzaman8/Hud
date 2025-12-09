import jwt
import datetime

secret = "Booooooooooooooooom"
def create_token(payload):
    return (jwt.encode(payload, secret, algorithm="HS256"))

def decode_token(token):
    payload = jwt.decode(token, secret, algorithms= "HS256")
    return(payload)

a = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJleHAiOjE3NjUzMDg2ODgsImlhdCI6MTc2NTMwNTA4OH0.N7bInVQZiwatnuDoLLeM3avSpF4Aip4FFLGtMiVxuuI"
print(decode_token(a))



        
        
        
        
        

        
        # preferences = Preferences.objects.filter(user=user)
        # print("BOOOOOOOOOOOOOOOOOOOOOOOM")