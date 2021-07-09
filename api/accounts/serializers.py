from rest_framework.serializers import ModelSerializer, CharField, Serializer
from accounts.models import User


# noinspection PyAbstractClass
class VerifySerializer(Serializer):
    code = CharField(max_length=6)

    class Meta:
        fields = ('code',)

        extra_kwargs = {
            'code': {
                'write_only': True
            }
        }


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_verified')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'is_verified': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
