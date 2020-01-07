import jwt
import json
import bcrypt

from .models import (
    ProductMainCategories, 
    ProductSubCategories, 
    Brands,
    Products,
    ProductInfo,
    ProductSubImages,
    ProductOptionTitles, 
    ProductOptionDetails,
    OrderStatus,
    Orders,
    ProductReviews,
    ProductQuestions,
    ProductAnswers,
    UserLikeProducts
)

from django.views import View
from django.http  import JsonResponse
from datetime     import datetime, timedelta

class MainGetView(View):
    def get(self, request):
        offset       = request.GET.get("period_end", 50)
        period_start = datetime.now()
        period_end   = period_start + timedelta(days = offset)
        products     = (
            Products
            .objects
            .select_related("product_info")
            .prefetch_related("user_like_products")
            .filter(end_date__range = (period_start, period_end))[:offset]
        )

        goods = [{
            'id'        : product.id,
            'title'     : product.name,
            'date'      : product.start_date,
            'image'     : product.product_info.main_image,
            'desc'      : product.product_info.main_text,
            'like_count' : product.user_like_products_set.all().count(),
            'orders'    : Orders.objects.filter(product_id = product.id).count(),
            'like'      : False
        } for product in products]
        
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

        result = {
            "goods"         : goods,
            "steady_seller" : steadyseller,
            "present"       : present,
            "household"     : household,
            "order_closed"  : orderclosed 
        }
        return JsonResponse(result, safe=False, status = 200)

