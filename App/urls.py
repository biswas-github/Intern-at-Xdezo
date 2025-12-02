from django.urls import path,include
from . views import test

# url patterns for the app
urlpatterns = [
    
    path('test/',test)
]
