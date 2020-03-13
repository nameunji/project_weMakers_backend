import jwt
import json
import bcrypt

from .models    import *
from user.utils import login_decorator

from datetime            import datetime, timedelta
from django.forms.models import model_to_dict
from django.views        import View
from django.http         import JsonResponse, HttpResponse

class MainGetView(View):
    def get(self, request, event_id):
        products = EventProduct.objects.select_related('product').filter(event_id = event_id)
        goods = [{
            'id'         : product.product.id, 
            'title'      : product.product.name,
            'date'       : product.product.start_date,
            'image'      : ProductInfo.objects.get(product_id = product.product_id).main_image,
            'desc'       : ProductInfo.objects.get(product_id = product.product_id).main_text,
            'likeCount' : UserLikeProducts.objects.filter(product_id = product.product_id).count(),
            'orders'     : Orders.objects.filter(product_id = product.product_id).count(),
        } for product in products]

        return JsonResponse({"result": goods}, status=200)

class DetailView(View):
    def get(self, request, product_id):
        product = Products.objects.prefetch_related('productsubimages_set').select_related('main_category','sub_category').get(id=product_id)
        result = {
            'id'              : product.id,
            'name'            : product.name, 
            'price'           : int(product.price),
            'delivery_charge' : int(product.delivery_charge),
            'delivery_date'   : product.delivery_date.strftime("%Y-%m-%d"),
            'end_date'        : (product.end_date.date() - datetime.now().date()).days,
            'minimum_count'   : product.minimum_count,
            'maximum_count'   : product.maximum_count,
            'main_category'   : product.main_category.name,
            'sub_category'    : product.sub_category.name,
            'sub_image'       : list(product.productsubimages_set.all().values_list('sub_image', flat=True))
        }

        return JsonResponse(result, safe=False, status=200)


class DetailInfoView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id = product_id)
        result = {
            'detail_content' : product.detail_content,
            'info_detail'    : product.info_detail
        }
        return JsonResponse(result, safe=False, status=200)


class DetailReviewView(View):
    def get(self, request, product_id):
        offset = int(request.GET.get('offset',0))
        limit  = int(request.GET.get('limit', 10))
        
        reviews = ProductReviews.objects.select_related('user').filter(product_id = product_id).order_by('-created_at')[offset*limit : (offset+1)*limit]

        result = [{
            'nickname'   : review.user.nickname,
            'created_at' : review.created_at.strftime("%Y-%m-%d"),
            'content'    : review.content,
            'image'      : review.image
        } for review in reviews]
        
        return JsonResponse({"result": result}, status = 200)

    @login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        user = request.user
        if "image" in data : 
            ProductReviews(
                product_id = product_id,
                user       = user,
                content    = data["content"],
                grade      = data["grade"], 
                image      = data["image"]
            ).save()
        else:
            ProductReviews(
                product_id = product_id,
                user       = user,
                content    = data["content"],
                grade      = data["grade"], 
            ).save()

        return HttpResponse(status = 200)


class DetailQnaView(View):
    def get(self, request, product_id):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))

        questions = ProductQuestions.objects.prefetch_related('productanswers_set').filter(product_id = product_id)[offset*limit : (offset+1)*limit]
        results = []
        for question in questions:
                answer = question.productanswers_set.filter(question_id = question.id)
                if answer.exists():
                    results.append({
                        "id"         : question.id,
                        "content"    : question.content,
                        "nickname"   : question.user.nickname,
                        "updated_at" : question.updated_at.strftime("%Y-%m-%d %H:%M"),
                        "answer"     : answer[0].content
                    })
                else:
                    results.append({
                        "id"         : question.id,
                        "content"    : question.content,
                        "nickname"   : question.user.nickname,
                        "updated_at" : question.updated_at.strftime("%Y-%m-%d %H:%M")
                    })
        
        if 'Authorization' in request.headers:
            @login_decorator
            def addAuth(self, request, product_id, results):
                user = request.user
                userQuestion = ProductQuestions.objects.filter(product_id = product_id, user_id = user)
                
                for element in userQuestion:
                    for result in results:
                        if element.id == result["id"]:
                            result["user"] = True
                        if "user" not in result:
                            result["user"] = False
            
            addAuth(self, request, product_id, results)

        return JsonResponse({"result": results}, status = 200)

    @login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        user = request.user

        try:
            ProductQuestions(
                product_id = product_id,
                user       = user,
                content    = data["content"]
            ).save()
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
    
    @login_decorator
    def delete(self, request):
        try:
            question_id = request.GET.get('question')
            question = ProductQuestions.objects.get(id = question_id)
            answer = ProductAnswers.objects.filter(question_id = question.id)

            if answer.exists():
                answer[0].delete()
            question.delete()
            return HttpResponse(status = 200)

        except ProtectedError:
            return JsonResponse({'message':'CAN_NOT_QUESTION'}, status = 400)
        except ProductQuestions.DoesNotExist:
            return JsonResponse({'message':'INVALID_QUESTION'}, status = 400)


class DetailBrandView(View):
    def get(self, request, product_id):
        product = Products.objects.select_related('brand').get(id = product_id)
        
        return JsonResponse(model_to_dict(product.brand), safe=False, status=200)


class DetailOptionView(View):
    def get(self, request, product_id):
        try:
            titles = ProductOptionTitles.objects.prefetch_related('productoptiondetails_set').filter(product_id=product_id)

            result = [{
                "title"  : title.option_title,
                "option" : [{
                    "name"  : option.option_detail,
                    "price" : int(option.price)
                } for option in title.productoptiondetails_set.filter(product_option_title_id = title.id)]
            } for title in titles]

            return JsonResponse({"result": result}, status = 200)
        except IndexError:
            return JsonResponse({"message": "DOES_NOT_OPTION"}, status = 400)


class DetailRecommendItemView(View):
    @login_decorator
    def get(self, request, product_id):
        period_start = datetime.now()
        period_end   = period_start + timedelta(days = 30)
        category_check = Products.objects.get(id = product_id).main_category
        user = request.user

        products = Products.objects.filter(end_date__range = (period_start, period_end), main_category_id = category_check).order_by('-end_date')[:6]

        result = [{
            "id"    : product.id,
            "name"  : product.name,
            "price" : int(product.price),
            "image" : product.productinfo_set.get(product_id=product.id).main_image,
            "like"  : UserLikeProducts.objects.filter(product_id=product.id, user_id = user).exists()
        } for product in products]

        return JsonResponse({"result" : result}, status = 200)


class LikeView(View):
    @login_decorator
    def post(self, request):
        product = request.GET.get('product_id')
        user    = request.user

        try:
            like = UserLikeProducts.objects.get(product_id = product, user = user)
            like.delete()
            result = False
        except UserLikeProducts.DoesNotExist:
            UserLikeProducts(
                product_id = product,
                user       = user
            ).save()
            result = True
        
        return JsonResponse({'message':result}, status = 200)



