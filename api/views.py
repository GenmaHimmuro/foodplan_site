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
        sub = serializer.save()
        return Response(
            {
                'id': sub.id,
                'price': str(sub.price) if sub.price is not None else None,
                'duration': sub.duration,
                'diet_type': sub.diet_type,
                'is_breakfast': sub.is_breakfast,
                'is_lunch': sub.is_lunch,
                'is_dinner': sub.is_dinner,
                'is_dessert': sub.is_dessert,
                'promotion': sub.promotion_id,
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

