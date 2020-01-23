import re
import jwt
import json
import bcrypt

from .models           import Users
from wemakers.settings import SECRET_KEY

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.db              import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        check_password  = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        nickname_length = 2

        try:
            validate_email(data["email"])
            if len(data["nickname"]) < nickname_length:
                return JsonResponse({'message':'NICKNAME_SHORT'}, status = 400)

            if Users.objects.filter(nickname = data["nickname"]).exists():
                return JsonResponse({'message':'DUPLICATION_NICKNAME'}, status = 400)
                
            if Users.objects.filter(email = data["email"]).exists():
                return JsonResponse({'message':'DUPLICATION_EMAIL'}, status = 400)

            if not check_password.match(data["password"]):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
            
            hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            Users(
                nickname = data["nickname"],
                email    = data["email"],
                password = hashed_password.decode('utf-8')
            ).save()
            return HttpResponse(status = 200)

        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except IntegrityError:
            return JsonResponse({'message':'EXCEPTED_DATA'}, status= 401)

class AuthView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = Users.objects.get(email = data["email"])
            if bcrypt.checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status = 200)
            else:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
        except Users.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)



