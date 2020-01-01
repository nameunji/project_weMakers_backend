import jwt
import json
import bcrypt
import re

from django.views      import View
from django.http       import JsonResponse
from django.db         import IntegrityError
from wemakers.settings import SECRET_KEY
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models           import Users
from .utils            import login_decorator


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        check_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        try:
            validate_email(data["email"])
            if len(data["nickname"]) < 2 :
                return JsonResponse({'message':'NICKNAME_SHORT'}, status = 400)
            if len(data["password"]) < 8 :
                return JsonResponse({'message':'PASSWORD_SHORT'}, status = 400)
            if not check_password.match(data["password"]) :
                return JsonResponse({'message':'UNSATISFIED_PASSWORD'}, status = 400) 
            else :
                hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
                Users(
                    nickname = data["nickname"],
                    email    = data["email"],
                    password = hashed_password.decode('utf-8')
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        except ValidationError:
            return JsonResponse({'message':'NOT_EMAIL'}, status = 400 )
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except IntegrityError:
            return JsonResponse({'message':'EXCEPTED_DATA'}, status= 401)

class AuthView(View):
    def post(self, request):
        data = json.loads(request.body)
        check_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        try:
            validate_email(data["email"])
            user = Users.objects.get(email = data["email"])
            if not check_password.match(data["password"]) :
                return JsonResponse({'message':'UNSATISFIED_PASSWORD'}, status = 400)
            if bcrypt.checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status = 200)
            else:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
        except Users.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except ValidationError:
            return JsonResponse({'message': 'NOT_EMAIL'}, status = 400)
        except TypeError:
            return JsonResponse({'message': 'INVALID_VALUE'}, status = 400)



