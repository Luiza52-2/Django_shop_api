from django.contrib import admin
from django.urls import path, include
from product.views import (
    CategoryListCreateAPIView,
    CategoryDetailUpdateDeleteAPIView,
    ProductListCreateAPIView,
    ProductDetailUpdateDeleteAPIView,
    ReviewListCreateAPIView,
    ReviewDetailUpdateDeleteAPIView,
    ProductsWithReviewsAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/categories/', CategoryListCreateAPIView.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetailUpdateDeleteAPIView.as_view()),

    path('api/v1/products/', ProductListCreateAPIView.as_view()),
    path('api/v1/products/<int:id>/', ProductDetailUpdateDeleteAPIView.as_view()),

    path('api/v1/reviews/', ReviewListCreateAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailUpdateDeleteAPIView.as_view()),

    path('api/v1/products/reviews/', ProductsWithReviewsAPIView.as_view()),

    path('api/v1/users/', include('users.urls')),
]
