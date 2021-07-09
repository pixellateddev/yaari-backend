from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, VerifySerializer
from accounts.models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'activate':
            return VerifySerializer
        if self.action == 'refresh_verification':
            return Serializer
        return super(UserViewSet, self).get_serializer_class()

    def get_permissions(self, *args, **kwargs):
        if self.action == 'create':
            return [AllowAny(),]
        return super(UserViewSet, self).get_permissions(*args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super(UserViewSet, self).get_object()

    @action(detail=False, methods=['PUT'])
    def activate(self, request):
        code = request.POST['code']
        try:
            request.user.verify(code)
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=400)

    @action(detail=False, methods=['PATCH'])
    def refresh_verification(self, request):
        try:
            request.user.refresh_verification()
            return Response({'status': 'OK'})
        except ValidationError as error:
            return Response({'error': error.message}, status=400)
