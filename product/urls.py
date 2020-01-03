from django.urls import path
from .views      import MainGetView
urlpatterns = [
   path('', MainGetView.as_view()),
]
