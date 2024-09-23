from django.urls import path
from .views import view_Person, view_Hanja, view_Question

urlpatterns = [
    path('review/', view_Person.as_view(), name='review'),  
]
