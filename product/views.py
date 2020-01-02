import jwt
import json
import bcrypt
from datetime     import datetime, timedelta

from django.views import View
from django.http  import JsonResponse
from .models      import ProductMainCategories, ProductSubCategories, Brands, Products, ProductInfo, ProductSubImages, ProductOptionTitles, ProductOptionDetails, OrderStatus, Orders, ProductReviews, ProductQuestions, ProductAnswers, UserLikeProducts


class MainGetView(View):
    def get(self, request):

        period_start = datetime.now()
        period_end   = period_start + timedelta(days = 50)
        products = Products.objects.filter(end_date__range = (period_start, period_end)).all()

        goods_products = list(products)
        goods = [{
            'id'         : product.id, 
            'title'      : product.name,
            'date'       : product.start_date,
            'image'      : ProductInfo.objects.get(product_id = product.id).main_image,
            'desc'       : ProductInfo.objects.get(product_id = product.id).main_text,
            'likeCount' : UserLikeProducts.objects.filter(product_id = product.id).count(),
            'orders'     : Orders.objects.filter(product_id = product.id).count(),
            'like'       : False
            } for product in goods_products[:50]]
        
        steadyseller_products = list(products.order_by('price'))
        steadyseller = [{
            'id': product.id,
            'title': product.name,
            'orders': Orders.objects.filter(product_id = product.id).count(),
            'like': False,
            'likeCount': UserLikeProducts.objects.filter(product_id = product.id).count(),
            'image': ProductInfo.objects.get(product_id = product.id).main_image
            } for product in steadyseller_products[:10]]

        present_products = list(products.filter(name__contains = '선물'))
        present = [{
            'id': product.id,
            'title': product.name,
            'orders': Orders.objects.filter(product_id = product.id).count(),
            'like': False,
            'likeCount': UserLikeProducts.objects.filter(product_id = product.id).count(),
            'image': ProductInfo.objects.get(product_id = product.id).main_image
        } for product in present_products]

        household_products = list(products.filter(main_category_id=3))
        household = [{
            'id': product.id,
            'title': product.name,
            'orders': Orders.objects.filter(product_id = product.id).count(),
            'like': False,
            'likeCount': UserLikeProducts.objects.filter(product_id = product.id).count(),
            'image': ProductInfo.objects.get(product_id = product.id).main_image
        } for product in household_products]

        orderclosed_products = list(Products.objects.filter(end_date__lt = datetime.now()))
        orderclosed = [{
            'id': product.id,
            'title': product.name,
            'image': ProductInfo.objects.get(product_id = product.id).main_image
        } for product in orderclosed_products]

        result = {"goods": goods, "steadySeller": { "list": steadyseller}, "present":{ "list":present }, "household":{ "list":household }, "orderClosed": { "list":orderclosed }  }
        return JsonResponse(result, safe=False, status = 200)

