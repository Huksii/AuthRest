from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Product,Category
from .serializers import ProductSerializer, CategorySerializer, UserSerializer

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # AuthTokenSerializer > обрабатывает данные запроса(username, password, token) и возвращает объект токена.
        serializer = self.serializer_class(data=request.data, context={'request': request})
        context ={'request': request}
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'message': 'Токен создан'
            })
        else:
            token.created = timezone.now()
            token.save()
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'message': 'Токен обновлен'
            })

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user) #(True, False)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={200: 'Список продуктов',},
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'price', 'stock', 'description', 'category'],  # обязательные поля
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название продукта'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Цена продукта'),
                'stock': openapi.Schema(type=openapi.TYPE_NUMBER, description='Количество товара'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание продукта'),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Категория продукта'),
            },
        ),
        responses={201: 'Создание продукта', 400: 'Ошибка при создании продукта'},
    )
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        context = {
            "errors": serializer.errors,
            "message": "Произошла ошибка"
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get_product(self, pk):
        try:
            return Product.obj.get(pk=pk)
        except Product.DoesNotExist:
            context = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"Продукт с таким id={id} не найден"
            }
            return context
        
    def get(self, request, id):
        product = self.get_product(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'price', 'stock', 'description', 'category'],  # обязательные поля
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название продукта'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Цена продукта'),
                'stock': openapi.Schema(type=openapi.TYPE_NUMBER, description='Количество товара'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание продукта'),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Категория продукта'),
            },
        ),
        responses={200: 'Продукт успешно обновлён',
                   400: 'Ошибка при обновлении продукта'}
    )
    def put(self, request, id):
        product = self.get_product(id)
        serializer = ProductSerializer(product)
        instance = ProductSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        product = self.get_product(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryListViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'Список категории',},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: 'Category created successfully',
            400: 'Bad request. Check the request data.',
        },
    )
    def post(self, request):
        """
        Create a new category.
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist as CategoryDoesNotExist:
            return Response({"message": f"{CategoryDoesNotExist}"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)  
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],  # обязательные поля
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название категории'),
            },
        ),
        responses={200: 'Категория успешно обновлена',
                   400: 'Ошибка при обновлении'}
    )
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist as CategoryDoesNotExist:
            return Response({"message": f"{CategoryDoesNotExist}"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist as CategoryDoesNotExist:
            return Response({"message": f"{CategoryDoesNotExist}"}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

