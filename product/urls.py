from django.urls import path
from .views      import (
   MainGetView,
   DetailView,
   DetailInfoView,
   DetailReviewView,
   DetailQnaView,
   DetailBrandView,
   DetailOptionView,
   DetailRecommendItemView,
   LikeView,
)

urlpatterns = [
   path('', MainGetView.as_view()),
   path('/<int:product_id>', DetailView.as_view()),
   path('/<int:product_id>/info', DetailInfoView.as_view()),
   path('/<int:product_id>/review', DetailReviewView.as_view()),
   path('/<int:product_id>/qna', DetailQnaView.as_view()),
   path('/<int:product_id>/brand', DetailBrandView.as_view()),
   path('/<int:product_id>/option', DetailOptionView.as_view()),
   path('/<int:product_id>/recommend', DetailRecommendItemView.as_view()),
   path('/like', LikeView.as_view()),
]
