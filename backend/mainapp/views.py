from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import re, jwt, json, datetime
from mainapp.utils import jwt_utils 
from .models import UserPreferences,PreferenceCategory, SavedNews
import requests
from itertools import product
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs

def getUser(request):
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

def generate_newsapi_urls(preferences):
    api_key = "269e2c11b227414faccf57211539c6d6"
    base_url = "https://newsapi.org/v2/everything?"
    urls = []

    for pref in preferences:
        params = {
            "q": pref.topics,
            "language": pref.language,
            "apiKey": api_key,
        }
        url = base_url + urlencode(params)

        urls.append({
            "url": url,
            "category": pref.category.category,
            "topic": pref.topics
        })

    return urls

def find_q (url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    return query_params.get("q", [""])[0]


#frontend request
# {
#   "category": "Technology",
#   "topic": "AI",
#   "article": {
#     "title": "Mozilla announces an AI ‘window’ for Firefox",
#     "url": "https://www.theverge.com/news/820196/mozilla-firefox-ai-window-browser",
#     "source": "The Verge",
#     "description": "Another day, another AI browser...",
#     "published_at": "2025-11-13T17:26:41Z"
#   }
# }

@csrf_exempt
def save_news(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method does not allowed"
        }, status=400)
    
    user, error = getUser(request)
    if error:
        return error
    
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({
            "success" : False, 
            "message": "Invalid json"
        }, status=400)
    
    article = body.get('article')
    if not article:
        return JsonResponse({
            "success":False, 
            "message" : "Missing article data"
        }, status=400)
    
    required_fields = ["title", "url", "published_at"]
    for field in required_fields:
        if field not in article:
            return JsonResponse({
                "success":False, 
                "message":f"Missing article field: {field}"
            }, status=404)
        
    try:
        saved, created = SavedNews.objects.get_or_create(
            user=user,
            url=article["url"],
            defaults={
                "title": article["title"],
                "source": article["source"],
                "description": article.get("description"),
                "published_at": article.get("published_at"),
            }
        )
    except Exception:
        return JsonResponse({
            "success": False,
            "message": "Something went wrong. Failed to save article"
        }, status=500)
    
    if not created:
        return JsonResponse({
            "success": False,
            "message": "Article already saved"
        }, status=409)

    return JsonResponse({
        "success": True,
        "message": "Article saved successfully"
    }, status=201)

@csrf_exempt
def get_saved_news(request):
    if request.method != "GET":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    user, error = getUser(request)
    if error:
        return error

    saved_news = SavedNews.objects.filter(user=user)

    if not saved_news.exists():
        return JsonResponse({
            "success": False,
            "message": "No bookmarked news found for this user"
        }, status=404)

    result = []
    for news in saved_news:
        result.append({
            "id": news.id,
            "title": news.title,
            "url": news.url,
            "source": news.source if news.published_at else None,
            "description": news.description,
            "published_at": news.published_at.isoformat() if news.published_at else None,
            "saved_at": news.saved_at.isoformat(),
        })

    return JsonResponse({
        "success": True,
        "message": "News fetched successfully",
        "count": len(result),
        "news": result
    }, status=200)

@csrf_exempt
def delete_saved_news(request, news_id):
    if request.method != "DELETE":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    user, error = getUser(request)
    if error:
        return error

    try:
        news = SavedNews.objects.get(id=news_id, user=user)
    except SavedNews.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Saved news not found"
        }, status=404)

    news.delete()

    return JsonResponse({
        "success": True,
        "message": "Saved news deleted successfully"
    }, status=200)

@csrf_exempt
def delete_all_saved_news(request):
    if request.method != "DELETE":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    user, error = getUser(request)
    if error:
        return error

    queryset = SavedNews.objects.filter(user=user)

    if not queryset.exists():
        return JsonResponse({
            "success": False,
            "message": "No saved news found for this user"
        }, status=404)

    deleted_count, _ = queryset.delete()

    return JsonResponse({
        "success": True,
        "message": "All saved news deleted successfully",
        "deleted_count": deleted_count
    }, status=200)

@csrf_exempt
def get_news(request):
    if request.method != "GET":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    # Authenticate user via JWT cookie
    user, error = getUser(request)
    if error:
        return error

    # Fetch preferences
    preferences = (
        UserPreferences.objects
        .filter(user=user)
        .select_related("category")
    )

    if not preferences.exists():
        return JsonResponse({
            "success": False,
            "message": "No preferences found for this user."
        }, status=404)

    articles = []
    urls = generate_newsapi_urls(preferences)

    for item in urls:
        try:
            response = requests.get(item["url"], timeout=5)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            continue  # fail gracefully for one API failure

        articles.append({
            "category": item["category"],
            "topic": item["topic"],
            "articles": data.get("articles", [])[:6]
        })

    return JsonResponse({
        "success": True,
        "total_urls": len(urls),
        "results": articles
    }, status=200)

@csrf_exempt
def get_user_preferences(request):
    user, error = getUser(request)
    if error:
        return error

    if request.method != "GET":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    # Fetch all preference rows for this user
    preferences = UserPreferences.objects.filter(user=user).select_related("category")

    if not preferences.exists():
        return JsonResponse({
            "success": False,
            "message": "No preferences found for this user."
        }, status=404)

    # Serialize each preference entry
    data = []
    for pref in preferences:
        data.append({
            "id": pref.id,
            "category": pref.category.category,   # category name
            "topics": pref.topics,
            "sources": pref.sources,
            "region": pref.region,
            "language": pref.language
        })

    return JsonResponse({
        "success": True,
        "count": len(data),
        "data": data
    }, status=200)

# [
#     { "category": "Technology",
#       "topics": "AI", "sources": "",
#       "region": "global",
#       "language": "en"
#     },
#     { "category": "Football",
#      "topics": "Hamza",
#       "sources": "",
#        "region": "global",
#         "language": "en" 
#     }, 
#     { "category": "Politics", "topics": "BD Politics", "sources": "", "region": "global", "language": "en" }, 
#     { "category": "Badminton", "topics": "Kim Jong Woong", "sources": "", "region": "global", "language": "en" }, 
#     { "category": "Football", "topics": "Ronaldo", "sources": "", "region": "global", "language": "en" }
# ]

# Issue in add_user_preferences
# If one item fails, the entire request stops.
# Better:
# Validate all
# Insert valid ones
# Return partial success

@csrf_exempt
def add_user_preferences(request):
    user, error = getUser(request)
    if error:
        return error

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    # Parse list of objects
    try:
        preferences_list = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON format"
        }, status=400)

    if not isinstance(preferences_list, list):
        return JsonResponse({
            "success": False,
            "message": "Request body must be a list of preference objects"
        }, status=400)

    created_items = []

    for item in preferences_list:
        category_name = item.get("category")
        topics = item.get("topics")
        # sources = item.get("sources", "")
        # region = item.get("region", "global")
        # language = item.get("language", "en")

        # Validate required fields
        if not category_name or not topics:
            return JsonResponse({
                "success": False,
                "message": "Each item must contain at least 'category' and 'topics'"
            }, status=400)

        # 1. Ensure category exists for user
        category_obj, _ = PreferenceCategory.objects.get_or_create(
            user=user,
            category=category_name.strip()
        )

        # 2. Create or get the user preference
        pref, created = UserPreferences.objects.get_or_create(
            user=user,
            category=category_obj,
            topics=topics.strip(),
            # sources=sources.strip(),
            # defaults={
            #     "region": region,
            #     "language": language
            # }
        )

        if created:
            created_items.append({
                "category": category_name,
                "topics": topics,
                # "sources": sources,
                # "region": region,
                # "language": language
            })

    return JsonResponse({
        "success": True,
        "message": "Preferences processed successfully",
        "created_count": len(created_items),
        "created": created_items
    }, status=201)

# {
#     "category": "Football",
#     "topics": "Hamza"
# }

@csrf_exempt
def delete_user_preference(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    user, error = getUser(request)
    if error:
        return error

    # Parse JSON body
    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON body"
        }, status=400)

    # category_name = body.get("category")
    # topic_name = body.get("topics")
    id = body.get("id")

    # if not category_name or not topic_name:
    #     return JsonResponse({
    #         "success": False,
    #         "message": "'category' and 'topics' fields are required"
    #     }, status=400)

    if not id :
        return JsonResponse({
            "success": False,
            "message": "'ID' fields are required"
        }, status=400)    

    # Step 2: Find the specific preference row 
    try:
        pref = UserPreferences.objects.get(
            id = id
        )
    except UserPreferences.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Topic not found for this category"
        }, status=404)

    # Step 3: Delete only the topic row
    pref.delete()

    return JsonResponse({
        "success": True,
        #"message": f"Topic '{topic_name}' removed from category '{category_name}'"
    }, status=200)

@csrf_exempt
def delete_all_preferences(request):
    # Authenticate user
    user, error = getUser(request)
    if error:
        return error

    # Validate method
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)

    # Fetch all preferences for the user
    prefs = UserPreferences.objects.filter(user=user)
    print(prefs)
    if not prefs:
        return JsonResponse({
            "success": False,
            "message": "No preferences found for this user"
        }, status=404)

    # Delete all preference rows
    prefs.delete()

    return JsonResponse({
        "success": True,
        "message": "All preference records deleted successfully.",
    }, status=200)

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
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
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

# fetch("/api/logout/", {
#   method: "POST",
#   credentials: "include"
# });

# How does logout work in JWT authentication?
# JWT is stateless, so logout does not invalidate the token server-side.
# Logout works by removing the JWT from client storage (cookie or localStorage).
# For higher security, token blacklisting or short-lived access tokens with refresh tokens are used.
@csrf_exempt
def logout(request):
    response = JsonResponse({
        "success": True,
        "message": "Logged out successfully"
    })

    response.delete_cookie(
        key="access",
        path="/",
        samesite="Lax"
    )

    return response

# {
#     "success": False,
#     "message": "Categories fetched successfully",
#     "categories": [
#         {
#             "category": "Technology"
#         },
#         {
#             "category": "Sports"
#         },
#         {
#             "category": "Politics"
#         },
#         {
#             "category": "Football"
#         },
#         {
#             "category": "GeoPolitics"
#         },
#         {
#             "category": "Badminton"
#         },
#         {
#             "category": "technology"
#         },
#         {
#             "category": "science"
#         },
#         {
#             "category": "Football"
#         },
#         {
#             "category": "Politics"
#         },
#         {
#             "category": "Badminton"
#         },
#         {
#             "category": "Technology"
#         },
#         {
#             "category": "Badminton"
#         }
#     ]
# }


from django.views.decorators.http import require_GET
@require_GET
def get_categories(request):
    user, error = getUser(request)
    if error:
        return error

    categories = PreferenceCategory.objects.all()

    if not categories.exists():
        return JsonResponse({
            "success": False,
            "message": "No categories found",
        }, status=404)

    # Extract category strings
    result = [{"category": cat.category} for cat in categories]

    return JsonResponse({
        "success": True,
        "message": "Categories fetched successfully",
        "categories": result,
    }, status=200)