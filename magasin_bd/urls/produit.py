from django.urls import path
from magasin_bd.api.produit import ProduitList, ProduitGet, AchatParProduitList, ProduitApprovisionner

urlpatterns = [
    path('produites/', ProduitList.as_view()),
    path('produites/<int:id>/', ProduitGet.as_view()),
    path('par_produites/', AchatParProduitList.as_view()),
    path('approvisioner/<int:id>/', ProduitApprovisionner.as_view()),
]