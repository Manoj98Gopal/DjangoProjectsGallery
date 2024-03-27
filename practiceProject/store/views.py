from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .models import Product,Collection
# Create your views here.


@api_view(['GET','POST'])
def product_list(request):
    
    if request.method == 'GET':
        # here passing the releated filed to getting the info of collection
        queary = Product.objects.select_related('collection').all()[:10]
        serialize = ProductSerializer(queary,many=True)
        return Response(serialize.data)
    elif request.method == 'POST':
        serialize = ProductSerializer(data=request.data)
        return Response('oK')
        


@api_view()
def product_details(request,id):
    
    # this is long code actully
    # try:
    #     product = Product.objects.get(pk=id)
    #     serialize = ProductSerializer(product)
    #     return Response(serialize.data)
    # except Product.DoesNotExist:
    #     return Response({'message':'product does not exist'},status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     return Response({'message':str(e)},status=500)
    
    # this is short code 
    
    product = get_object_or_404(Product,pk=id)
    serialize = ProductSerializer(product)
    return Response(serialize.data)