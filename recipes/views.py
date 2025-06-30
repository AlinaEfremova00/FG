from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe, Tag, Ingredient, Favorite, ShoppingCart
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()

        if request.method == 'POST':
            obj, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            if created:
                serializer = FavoriteSerializer(obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'detail': 'Уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            deleted, _ = Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': 'Не было в избранном'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()

        if request.method == 'POST':
            obj, created = ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
            if created:
                serializer = ShoppingCartSerializer(obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'detail': 'Уже в корзине'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            deleted, _ = ShoppingCart.objects.filter(user=request.user, recipe=recipe).delete()
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': 'Не было в корзине'}, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
