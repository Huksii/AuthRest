from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListViews, \
    CategoryDetailView, CustomObtainAuthToken, CreateUserView


urlpatterns = [
    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/', CategoryListViews.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]