from django.urls import path
from .views import *
urlpatterns= [
    path("verhalen/", VerhalenList.as_view(), name="verhalen-list"),
    path("verhalen/<int:pk>/", VerhalenDetail.as_view(), name="verhalen-detail"),
    path("verhalen/admin/", VerhalenListAdmin.as_view(), name="verhalen-list-admin"),
    path("verhalen/admin/<int:pk>", VerhalenDetailAdmin.as_view(), name="verhalen-detail-admin"),
    path("categorieen/", CategorieList.as_view(), name="categorieen-list"),
    path("categorieen/admin/", CategorieListAdmin.as_view(), name="categorieen-list-admin"),
    path("categorieen/admin/<int:pk>", CategorieDetailAdmin.as_view(), name="categorieen-detail-admin"),
]
