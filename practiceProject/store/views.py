from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import ProductSerializer,CollectionSerializer,ReviewSerializer
from .models import Product,Collection,Review
# Create your views here.


# class based api
class ProductList(APIView):
        
    def get(self,request):
        queary = Product.objects.all()
        # use get method becouse if collection_id is not there it is giving none 
        # if you access normally it will crash more chances
        collection_id = request.query_params.get('collection_id')
        # print("-----------------",collection_id)
        if collection_id is not None:
            queary = queary.filter(collection_id=collection_id)
            
        serialize = ProductSerializer(queary,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
        
    
    def post(self,request):
        serialize = ProductSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data,status=status.HTTP_201_CREATED)    
    
    
    
class ProductDetails(APIView):
    
    def get(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serialize = ProductSerializer(product)   
        return Response(serialize.data,status=status.HTTP_200_OK) 
    
    def put(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serialize = ProductSerializer(product,data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        product = get_object_or_404(Product,pk=id)
        if product.orderitems.count() > 0:
            return Response({'error':"product cannot be deleted"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message':"product deleted"},status=status.HTTP_200_OK)
    
    
    
    
    
class CollectionList(APIView):
    
    def get(self,request):
        queary = Collection.objects.all()
        serializer = CollectionSerializer(queary,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def post(self,request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    
class CollectionDetails(APIView):
    
    def get(self,request,id):
        collection = get_object_or_404(Collection,pk=id)
        serializer = CollectionSerializer(collection)    
        return Response(serializer.data)
    
    
    def put(self,request,id):
        collection = get_object_or_404(Collection,pk=id)
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def delete(self,request,id):
        collection = get_object_or_404(Collection,pk=id)
        collection.delete()
        return Response({'message':"collection deleted"},status=status.HTTP_200_OK)
    
    
    
class ReviewList(APIView):
    
    def get(self,request):
        queary = Review.objects.all()
        serializer = ReviewSerializer(queary,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def post(self,request):
        serializer = ReviewSerializer(data=request.data)   
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class ReviewDetails(APIView):
    
    def get(self,request,id):
        review = get_object_or_404(Review,pk=id)   
        serializer = ReviewSerializer(review) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        review = get_object_or_404(Review,pk=id)
        serializer = ReviewSerializer(review,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        review = get_object_or_404(Review,pk=id)
        review.delete()
        return Response({"message":"Successfully deleted"},status = status.HTTP_200_OK)
        



# function based api
@api_view(['GET','POST'])
def product_list(request):
    
    if request.method == 'GET':
        # here passing the releated filed to getting the info of collection
        queary = Product.objects.select_related('collection').all()[:2]
        serialize = ProductSerializer(queary,many=True)
        return Response(serialize.data)
    elif request.method == 'POST':
        serialize = ProductSerializer(data=request.data)
        
        # here befor validated_data we need to check is_valid 
        # this is also one of the way to handle the error  another way also is there 
        # if serialize.is_valid():
        #     print(serialize.validated_data)
        #     return Response('oK')
        # else:
        #     return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        # this is also checking is_valid  with efficent way
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data,status=status.HTTP_201_CREATED)
        


@api_view(['GET','PUT','DELETE'])
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
    if request.method == 'GET':
        serialize = ProductSerializer(product)
        return Response(serialize.data)
    elif request.method == 'PUT':
        # for updateing the record we need to pass product object to serializer
        serialize = ProductSerializer(product,data=request.data)
        serialize.is_valid(raise_exception = True)
        serialize.save()
        return Response(serialize.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error':"product cannot be deleted"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message':"product deleted"},status=status.HTTP_200_OK)





    
    
@api_view(['GET','POST'])    
def collection_list(request):    
    
    if request.method == 'GET':
        queary = Collection.objects.all()
        # queary = Collection.objects.annotate(product_count=Count('products')).all()        
        serializer = CollectionSerializer(queary,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
@api_view(['GET','PUT','DELETE'])    
def collection_detail(request,id):
    
    collection = get_object_or_404(Collection,pk=id)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = CollectionSerializer(collection,data=request.data)    
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == "DELETE":
        collection.delete()
        return Response({'message':"collection deleted"},status=status.HTTP_200_OK)