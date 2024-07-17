from django.urls import path
from .views import view_Person, view_Hanja, view_Question

urlpatterns = [
    path('person/', view_Person.as_view(), name='person'),  
    path('hanja/', view_Hanja.as_view(), name='hanja'),  
    path('question/', view_Question.as_view(), name='question'),  
]
