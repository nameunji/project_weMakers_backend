import jwt
import json
import bcrypt
import re

from django.views           import View
from django.http            import JsonResponse
from django.db              import IntegrityError
from wemakers.settings      import SECRET_KEY
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Users
from .utils  import login_decorator

ALPHANUMERIC_EIGHT_CHARS = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

class UserView(View):
    def post(self, request):
        data           = json.loads(request.body)
        check_password = re.compile(ALPHANUMERIC_EIGHT_CHARS)

        try:
            validate_email(data["email"])
            
            if len(data["nickname"]) < 2 :
                return JsonResponse({'message':'NICKNAME_SHORT'}, status = 400)
            if not check_password.match(data["password"]) :
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400) 

            hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

            if Users.objects.exist(email = data["email"]):
                return JsonResponse({"error" : "EMAIL_ALREADY_EXISTS"}, status=401)
            if Users.objects.exist(nickname = data["nickname"]):
                return JsonResponse({"error" : "NICKNAME_EXISTS"}, status=401)

            Users(
                nickname = data["nickname"],
                email    = data["email"],
                password = hashed_password.decode('utf-8')
            ).save()

            return HttpResponse(status=200)
        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL'}, status=400 )
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class AuthView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = Users.objects.get(email = data["email"])

            if bcrypt.checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status = 200)

            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
        except Users.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except TypeError:
            return JsonResponse({'message': 'INVALID_PAYLOAD'}, status = 400)
