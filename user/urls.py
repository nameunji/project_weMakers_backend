from django.urls import path
from .views      import UserView, AuthView

urlpatterns = [
   path('', UserView.as_view()),
   path('/auth', AuthView.as_view()),
]
