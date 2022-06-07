from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin_bd.models.achat import Achat
from magasin_bd.serializers.achat import AchatSerializer, AchatPostSerializer
from magasin_bd.models.produit import Produit
from magasin_bd.serializers.produit import ProduitSerializer, ProduitQuantiteNewSerializer

class AchatList(APIView):

    def get(self, request):
        achats = Achat.objects.all()
        serializer = AchatSerializer(achats, many=True)
        return Response(serializer.data)


    def get_produit(self, id):
        try:
            return Produit.objects.get(id = id)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        data = request.data
        query = request.data
        produit = self.get_produit(data['produit'])
        serializer_produit = ProduitSerializer(produit).data
        if data['quantite'] > 0:   
            if data['quantite'] <= serializer_produit['quantite']:
                print("qt debut",data['quantite'])
                data['prix_total'] = serializer_produit['prix'] * data['quantite']
                serializer = AchatSerializer(data=data)
                if serializer.is_valid():
                    query['quantite'] = serializer_produit['quantite'] - data['quantite']
                    print("qt a jour stocke",query['quantite'])
                    serializer_produit = ProduitQuantiteNewSerializer(produit, data=query)
                    if serializer_produit.is_valid():
                        serializer.save()
                        serializer_produit.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer_produit.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'quantite insufisante'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'quantite est inferieur à 1'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        achats = Achat.objects.all()
        achats.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AchatGet(APIView):

    def get_object(self, id):
        try:
            return Achat.objects.get(id = id)
        except Achat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        achat = self.get_object(id)
        serializer = AchatSerializer(achat)
        return Response(serializer.data)


    def delete(self, request, id):
        achat = self.get_object(id)
        achat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)