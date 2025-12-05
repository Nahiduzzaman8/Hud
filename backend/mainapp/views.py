from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import re, jwt, json, datetime
from mainapp.utils import jwt_utils 

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                "success" : False, 
                "message" : "Error to fetch JSON data.", 
            }, status=400)

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        # 1. Required checks
        if not username:
            return JsonResponse({
                "success" :False, 
                "message" : "Username must be there.", 
            }, status=400)
        
        if not email:
            return JsonResponse({
                "success" :False, 
                "message" : "Email must be there.", 
            }, status=400)
        
        if not password:
            return JsonResponse({
                "success" :False, 
                "message" : "Password must be there.", 
            }, status=400)

        
        # 2. Username rules
        if len(username) < 3:
            return JsonResponse({
                "success" :False, 
                "message" : "Length of username must be greater than 3.", 
            }, status=400)
        
        if len(username) > 50:
            return JsonResponse({
                "success" :False, 
                "message" : "Length of username must be less than 50.", 
            }, status=400)

        # 3. Email format validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return JsonResponse({
                "success" :False, 
                "message" : "Invalid email format.", 
            }, status=400)

        # 4. Password strength
        if len(password) < 4:
            return JsonResponse({
                "success" :False, 
                "message" : "Password must be at least 4 characters.", 
            }, status=400)
            
        if password.isdigit():
            return JsonResponse({
                "success" :False, 
                "message" : "Password cannot be only numbers.", 
            }, status=400)
        
        if password.isalpha():
            return JsonResponse({
                "success" :False, 
                "message" : "Password must contain numbers or special characters.", 
            }, status=400)

        # 5. Unique username/email checks
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success" :False, 
                "message" : "Username is already taken.", 
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success" :False, 
                "message" : "Email is already registered.", 
            }, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )

        return JsonResponse({
            "success": True,
            "message": "User created successfully.",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=201)

    return JsonResponse({
            "success": True,
            "message": "Signup endpoint metadata fetched successfully.",
            "data": {
    "fields": {
      "username": {
        "type": "string",
        "required": True,
        "min_length": 3,
        "max_length": 50
      },
      "email": {
        "type": "email",
        "required": True
      },
      "password": {
        "type": "string",
        "required": True,
        "min_length": 4
      }
    }
  },
            "error": "null"
            })

@csrf_exempt
def login(request):
    if request.method == "POST":
        try :
            data = json.loads(request.body)
        except :
            return JsonResponse({
                "success" : False, 
                "message" : "Error to fetch JSON data.", 
            }, status=400)
        
        email = data.get("email", "").strip()
        password = data.get("password", "")
        if not email:
            return JsonResponse({
                "success" :False, 
                "message" : "Email must be there.", 
            }, status=400)
        
        if not password:
            return JsonResponse({
                "success" :False, 
                "message" : "Password must be there.", 
            }, status=400)
        
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return JsonResponse({
                "success" :False, 
                "message" : "Invalid email format.", 
            }, status=400)
        
        if len(password) < 4:
            return JsonResponse({
                "success" :False, 
                "message" : "Password must be at least 4 characters.", 
            }, status=400)
            
        if password.isdigit():
            return JsonResponse({
                "success" :False, 
                "message" : "Password cannot be only numbers.", 
            }, status=400)
        
        if password.isalpha():
            return JsonResponse({
                "success" :False, 
                "message" : "Password must contain numbers or special characters.", 
            }, status=400)
        
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({
                "success" :False, 
                "message" : "Invalid username or password", 
            }, status=400)

        payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        }
        token = jwt_utils.create_token(payload)
        return JsonResponse({
                "success": True,
                "message": "Login successful.",
                "data": {
                        "user": {
                                "id": user.id,
                                "username": user.username,
                                "email": user.email
                                    },
                        "tokens":{
                                "access": token
                                    }
                            }
                            } , status=200)
    
    return JsonResponse({
        "success" : False, 
        "message" : "Method does not allowed" 
    })


