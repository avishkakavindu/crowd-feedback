from rest_framework.views import APIView
from django.http import HttpResponseBadRequest
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from rest_framework.generics import ListAPIView

from api.utils.crowd import detectByImage
from api.serializers import *
from api.models import *

from .feedback import predict_sentiment


class CrowdAPIView(APIView):
    def post(self, request, *args, **kwargs):
        crowd_count = request.data.get('crowd_count')
        shop_id = request.data.get('shop_id')

        shop_exists = Shop.objects.filter(id=shop_id).exists()

        if not shop_exists:
            return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

        shop = Shop.objects.get(id=shop_id)
        shop.current_crowd = crowd_count
        shop.save()
        
        # Return the annotated image as the API response
        return Response({'detail': 'Record saved'})

    def get(self, request, *args, **kwargs):
        # Retrieve crowds of all shops
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)


class FeedbackAPIView(APIView):

    def get(self, request, product_name):
        try:
            product = get_object_or_404(Product, name_readonly=product_name)

            top_shops = Shop.objects.annotate(
                average_rating=Avg('feedback__rating',
                                   filter=models.Q(feedback__is_feedback_positive=True, feedback__product=product))
            ).order_by('-average_rating')[:3]

            top_shops_data = []
            for shop in top_shops:
                top_shops_data.append({
                    'shop_name': shop.name,
                    'location': shop.location,
                    'average_rating': shop.average_rating
                })

            return Response({'top_shops': top_shops_data})

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

    def post(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback_text = serializer.validated_data['feedback']

            sentiment_result = predict_sentiment(feedback_text)
            is_feedback_positive = (sentiment_result == "Positive")

            serializer.save(is_feedback_positive=is_feedback_positive)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ShopListView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer