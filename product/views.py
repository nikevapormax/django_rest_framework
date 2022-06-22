from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime

from .serializers import ProductSerializer

from .models import Product as ProductModel
from .models import Review as ReviewModel
from django_rest_framework.permissions import IsAuthenticatedPostAfterThreeDays
from django.db.models import Q

class ProductView(APIView):
    permission_classes = [IsAuthenticatedPostAfterThreeDays]
    
    # product 조회
    def get(self, request):
        # return Response({})
        
        today = datetime.now()
        products = ProductModel.objects.filter(Q(exposure_end__gte=today) & 
                                               Q(activate = True) |
                                               Q(user=request.user))
        
        product_serializer = ProductSerializer(products, many=True)
   
        return Response(product_serializer.data, status=status.HTTP_200_OK)
    
    # product 생성
    def post(self, request):
        # data = request.data.copy()
        # # request.data._mutable=True
        # data["user"] = request.user.id
        # print(data['user'])
        # print(data)
        
        user = request.user
        request.data["user"] = user.id
        print(request.data)

        product_serializer = ProductSerializer(data=request.data, context={"request": request})
        
        if product_serializer.is_valid(): 
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # prodcut 수정
    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        # fields에 있는 데이터를 다 넣을 필요가 없도록 하기 위해 partial=True 사용
        product_serializer = ProductSerializer(product, data=request.data, context={"request": request}, partial=True)
        
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request):
        return Response({"msg": "delete method!!"})