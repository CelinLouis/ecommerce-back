from django.urls import path
from magasin_bd.api.achat import AchatList, AchatGet

urlpatterns = [
    path('achats/', AchatList.as_view()),
    path('achats/<int:id>/', AchatGet.as_view()),
]