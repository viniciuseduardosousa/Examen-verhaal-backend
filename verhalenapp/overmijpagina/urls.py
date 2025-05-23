from django.urls import path
from .views import *

urlpatterns = [
    path('overmij/', Overmijview.as_view(), name='over-mij'),
    path('footer/', Footerview.as_view(), name='footer'),
    path('overmij/admin/', OvermijAdminview.as_view(), name='over-mij-admin'),
    path('footer/admin/', FooterAdminview.as_view(), name='footer-admin'),
]