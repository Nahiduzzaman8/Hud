from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import re, jwt, json, datetime
from mainapp.utils import jwt_utils 
from .models import User_preferences

def get_user_using_token(request):
    token = request.COOKIES.get('access')
    
    if not token:
        return None, JsonResponse({
            "success": False, 
            "message": "Token required"
            }, status=401)
    
    payload = jwt_utils.decode_token(token)
    if not payload:
        return None, JsonResponse({
            "success": False, 
            "message": "Payload is empty"
            }, status=400)
    user_id = payload["user_id"]

    if not user_id:
        return None, JsonResponse({"success": False, 
            "message": "No user id has been found"
            }, status=404)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, JsonResponse({
            "success": False, 
            "message": "No user has been found"
            }, status=404)
    
    return user, None

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
        
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({
                "success" :False, 
                "message" : "Invalid username or password", 
            }, status=400)
        
        if not user.check_password(password):
            return JsonResponse({
                                "success": False,
                                "message": "Invalid Email or Password"
                                }, status=400)

        payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=12),
        "iat": datetime.datetime.utcnow(),
        }
        token = jwt_utils.create_token(payload)

        response = JsonResponse(
            {
            "success": True,
            "message": "Login successful.",
            "data": {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token":token,
            }
        }, status=200)

        response.set_cookie(
            key="access",
            value=token,
            httponly=True,      # protect from XSS
            secure=False,       # True in production
            samesite="Lax",
            max_age=3600,
            path="/",
        )
        return response
    
    return JsonResponse({
        "success" : False, 
        "message" : "Method does not allowed" 
    }, status=400)

@csrf_exempt
def user_preferences(request): 
    user, error = get_user_using_token(request)
    if error:    
        return error

    if request.method == "GET":
        pref = User_preferences.objects.filter(user=user).first()
        if pref is None:
            return JsonResponse({
                "success": False,
                "message": "No preferences found for this user."
            }, status=404)
        
        
        return JsonResponse({
            "success": True,
            "data": {
                "id": pref.id,
                "categories": pref.categories,
                "topics": pref.topics,
                "sources": pref.sources,
                "region": pref.region,
                "language": pref.language
            }
        }, status=200)

    return JsonResponse({
        "success": False,
        "message": "Method not allowed"
    }, status=405)

@csrf_exempt
def add_user_preferences(request):
    if request.method == "POST":
        user, error= get_user_using_token(request)
        
        if error:
            return error
        
        pref, created = User_preferences.objects.get_or_create(user=user)

        try:
            body = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({
                "success": False,
                "message":"Invalid JSON"
            }, status = 400 )
        
        new_categories = body.get("categories", [])
        new_topics = body.get("topics", [])
        new_sources = body.get("sources", [])

        if "region" in body:    
            pref.region = body["region"]

        if "language" in body:
            pref.language = body["language"]
        
        # Validate types
        if not isinstance(new_categories, list) or not isinstance(new_topics, list) or not isinstance(new_sources, list):
                return JsonResponse({
                    "success":False,
                    "message": "categories/topics/sources must be lists"
                    }, status=400)
        
        # ADD (append, avoid duplicates)
        pref.categories = list(set(pref.categories + new_categories))
        pref.topics = list(set(pref.topics + new_topics))
        pref.sources = list(set(pref.sources + new_sources))

        pref.save()

        return JsonResponse({
            "success": True,
        "message": "Preference added successfully",
        "data": {
            "categories": pref.categories,
            "topics": pref.topics,
            "sources": pref.sources,
            "region": pref.region,
            "language": pref.language
        }
            }, status=201)
    
    return JsonResponse({
        "success":False,
        "message":"Method does not allowed"
    }, status=405)

@csrf_exempt
def remove_user_preference(request, pref_type):
    if request.method != "DELETE":
        return JsonResponse({
            "success":False, 
            "message":"Method not allowed"
        }, status=405)
    
    #validating preference type
    if pref_type not in ["categories", "topics", "sources"] :
        return JsonResponse({
            "success": False,
            "message":"Invalid preferences type" 
        }, status=400)
    
    #Extract value from the link
    value = request.GET.get("value")
    if not value:
        return JsonResponse({
            "success": False,
            "message": "Missing 'value' parameter"
        }, status=400)
    
    #fetching user
    user, error = get_user_using_token(request)
    if error:
        return error
    
    #fetching user preferences
    pref = User_preferences.objects.filter(user=user).first()
    if not pref:
        return JsonResponse({
            "success": False,
            "message": "No preferences found for this user"
        }, status=404)

    current_list = getattr(pref, pref_type)
    if value not in current_list:
        return JsonResponse({
            "success": False,
            "message": f"'{value}' not found in {pref_type}"
        }, status=404)
    
    current_list.remove(value)
    setattr(pref, pref_type, current_list)
    pref.save()

    return JsonResponse({
        "success": True,
        "message": f"{pref_type[:-1].capitalize()} removed successfully",
        "data": {
            "categories": pref.categories,
            "topics": pref.topics,
            "sources": pref.sources,
            "region": pref.region,
            "language": pref.language
        }
    }, status=200)


