from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import OrderSerializer, PromoCheckSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        return Response(
            {
                'id': subscription.id,
                'price': str(subscription.price) if subscription.price is not None else None,
                'duration': subscription.duration,
                'diet_type': subscription.diet_type,
                'is_breakfast': subscription.is_breakfast,
                'is_lunch': subscription.is_lunch,
                'is_dinner': subscription.is_dinner,
                'is_dessert': subscription.is_dessert,
                'promotion': subscription.promotion_id,
            },
            status=status.HTTP_201_CREATED,
        )


class PromoValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PromoCheckSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        price, applied = serializer.compute_price()
        return Response({'price': str(price), 'promo_applied': applied})
