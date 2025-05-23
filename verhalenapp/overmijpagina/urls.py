from django.urls import path
from .views import *

urlpatterns = [
    path('overmij/', Overmijview.as_view(), name='over-mij'),
    path('footer/', Footerview.as_view(), name='footer'),

]