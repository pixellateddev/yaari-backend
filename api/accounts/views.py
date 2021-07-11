from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User, PasswordUtils

from .serializers import (
    UserSerializer,
    VerifySerializer,
    ChangePasswordAnonymousSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    action_to_serializer_mapping = {
        'forgot_password': ForgotPasswordSerializer,
        'change_password': ChangePasswordSerializer,
        'change_password_anonymous': ChangePasswordAnonymousSerializer,
        'verify_user': VerifySerializer,
        'refresh_verification': Serializer
    }

    action_to_permission_mapping = {
        'create': [AllowAny(),],
        'change_password_anonymous': [AllowAny(),],
    }

    def get_serializer_class(self):
        serializer = self.action_to_serializer_mapping.get(
            self.action, super(UserViewSet, self).get_serializer_class()
        )
        return serializer

    def get_permissions(self, *args, **kwargs):
        permissions = self.action_to_permission_mapping(
            self.action, super(UserViewSet, self).get_permissions(*args, **kwargs)
        )

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super(UserViewSet, self).get_object()

    @action(detail=False, methods=['PUT'])
    def verify_user(self, request):
        code = request.data['code']
        try:
            request.user.verify(code)
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=400)

    @action(detail=False, methods=['PUT'])
    def refresh_verification(self, request):
        try:
            request.user.refresh_verification()
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=400)

    @action(detail=False, methods=['PUT'])
    def change_password(self, request):
        new_password = request.data['new_password']
        try:
            request.user.change_password(new_password)
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=400)

    @action(detail=False, methods=['PUT'])
    def change_password_anonymous(self, request):
        if request.user.is_authenticated:
            print('authenticated')
            return Response({'error': 'User already authenticated'}, status=400)

        code = request.data['code']
        new_password = request.data['new_password']

        obj = get_object_or_404(PasswordUtils, forgot_password_code=code)
        try:
            obj.change_password_anonymous(new_password)
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=error.code)

    @action(detail=False, methods=['PUT'])
    def forgot_password(self, request):
        username = request.data['username']
        if '@' in username:
            user = get_object_or_404(User, email=username)
        else:
            user = get_object_or_404(User, username=username)

        user.forgot_password()
        return Response({'status': 'OK'})

