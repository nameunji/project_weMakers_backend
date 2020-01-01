from django.urls import path
from .views      import UserView, AuthView, TestView
urlpatterns = [
   path('', UserView.as_view()),
   path('/auth', AuthView.as_view()),
   path('/test', TestView.as_view()),
]
