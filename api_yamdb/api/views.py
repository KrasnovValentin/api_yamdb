from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL

from reviews.models import Review, Comment, Title
from users.models import User, UserRole
from .permissions import (IsAdmin, IsSuperUser, AuthorOrAdminOrModeratorOrReadOnly)
from .serializers import (SendConfirmationCodeSerializer, SendTokenSerializer,
                          UpdateSelfSerializer, UserSerializer, 
                          CommentSerializer, ReviewSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Класс пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsSuperUser)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            url_path='me', permission_classes=[IsAuthenticated])
    def get_or_update_self(self, request):
        """
        Функция обрабатывает 'GET' и 'PATCH' запросы на эндпоинт '/users/me/'
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)
        serializer = UpdateSelfSerializer(
            instance=request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user_email = User.objects.filter(email=email).exists()
        user_username = User.objects.filter(username=username).exists()

        data_of_me = self.get_serializer(request.user, many=False)

        if user_email and email != data_of_me.data.get('email'):
            message = {'email': f'{email} уже зарегистрирован'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if user_username and username != data_of_me.data.get('username'):
            message = {'username': f'{username} уже зарегистрирован'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if (data_of_me.data.get('role') == UserRole.USER
                and 'role' in request.data):
            message = {'role': 'user'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

def send_email(email):
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(email=email).update(
        confirmation_code=confirmation_code
    )
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    """
    Функция обрабатывает POST-запрос для регистрации нового пользователя и
    получаения кода подтверждения, который необходим для получения JWT-токена.
    На вход подается 'username' и 'email', а в ответ происходит отправка
    на почту письма с кодом подтверждения.
    """
    serializer = SendConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user_email = User.objects.filter(email=email).exists()
    user_username = User.objects.filter(username=username).exists()

    if user_email:
        message = {'email': f'{email} уже зарегистрирован.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if user_username:
        message = {'username': f'{username} уже зарегистрирован.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if not (user_email or user_username):
        User.objects.create_user(email=email, username=username)
        send_email(email)
        message = {'email': email, 'username': username}
        return Response(message, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_token(request):
    """
    Функция обрабатывает POST-запрос для получаения JWT-токена.
    На вход подается 'username' и 'confirmation_code',
    а в ответ формируется JWT-токен.
    """
    serializer = SendTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    token = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        message = {'confirmation_code': 'Неверный код подтверждения'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    message = {'token': str(AccessToken.for_user(user))}
    return Response(message, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        AuthorOrAdminOrModeratorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'score']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [
        AuthorOrAdminOrModeratorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['text', 'pub_date']

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
        