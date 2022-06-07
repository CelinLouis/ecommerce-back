from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin_bd.serializers.produit import ProduitSerializer, ParProduitSerializer, ProduitQuantiteNewSerializer
from magasin_bd.models.produit import Produit
from magasin_bd.pagination import PaginationPageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q


class ProduitList(APIView):

    def get(self, request):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        data = request.data
        serializer = ProduitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        produits = Produit.objects.all()
        produits.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProduitGet(APIView):

    def get_obeject(self, id):
        try:
            return Produit.objects.get(id=id)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get_produit_name(self, name):
        try:
            return Produit.objects.get(nom=name)

        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produit = self.get_obeject(id)
        serializer = ParProduitSerializer(produit)
        return Response(serializer.data)


    def delete(self, request, id):
        produit = self.get_obeject(id)
        produit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, id):
        produit = self.get_object(id)
        data=request.data
        data['nom'] = data['nom'].upper()
        serializer = ProduitSerializer(produit, data=data)
        if serializer.is_valid():
            produit_existe = self.get_produit_name(data['nom'])
            if produit_existe == 0:
                serializer.save()
                return Response(serializer.data)
            else:
                this_produit = ProduitSerializer(produit).data 
                produit_existe = ProduitSerializer(produit_existe).data
                if this_produit['id'] == produit_existe['id']:
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message': 'Produit exciste deja'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AchatParProduitList(ListAPIView):
    serializer_class = ParProduitSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Produit.objects.all().order_by('-date_modification')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_cproduit__icontains=query)
            ).distinct()
        return queryset_list


class ProduitApprovisionner(APIView):

    def get_object(self, id):
        try:
            return Produit.objects.get(id=id)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produit = self.get_object(id)
        serializer = ParProduitSerializer(produit)
        return Response(serializer.data)


    def put(self, request, id):
        produit = self.get_object(id)
        this_produit = ProduitSerializer(produit).data 
        data=request.data
        qt = int(data['new_quantite'])
        if qt > 0:   
            data['quantite'] = this_produit['quantite'] + qt
            serializer = ProduitQuantiteNewSerializer(produit, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'quantite est inferieur à 1'}, status=status.HTTP_400_BAD_REQUEST)