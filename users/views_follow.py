from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User, Follow
from users.serializers_follow import FollowSerializer


class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list(self, request):
        follows = Follow.objects.filter(user=request.user)
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        author_id = request.data.get('author_id')
        if str(request.user.id) == str(author_id):
            return Response({'error': 'Нельзя подписаться на себя.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        follow, created = Follow.objects.get_or_create(user=request.user, author=author)
        if not created:
            return Response({'error': 'Уже подписаны.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        author_id = request.data.get('author_id')
        try:
            follow = Follow.objects.get(user=request.user, author__id=author_id)
        except Follow.DoesNotExist:
            return Response({'error': 'Вы не подписаны.'}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
