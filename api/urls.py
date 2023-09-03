from django.urls import path

from api.api_views import *

urlpatterns = [
    path('crowd', CrowdAPIView.as_view(), name='crowd_detection'),
    path('feedback', FeedbackAPIView.as_view(), name='feedback'),
    path('top_shops/<str:product_name>', FeedbackAPIView.as_view(), name='top_shops'),
    path('products', ProductListView.as_view(), name='product-list'),
    path('shops', ShopListView.as_view(), name='shop-list'),
]
