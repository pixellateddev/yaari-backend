from rest_framework.serializers import ModelSerializer, CharField, Serializer
from accounts.models import User


# noinspection PyAbstractClass
class VerifySerializer(Serializer):
    code = CharField(max_length=6)


class ForgotPasswordSerializer(Serializer):
    username_or_email = CharField(max_length=50, help_text='Username or Email of the user')


class ChangePasswordAnonymousSerializer(Serializer):
    code = CharField(max_length=12)
    new_password = CharField(max_length=30)

    class Meta:
        fields = '__all__'
        extra_kwargs = {
            'new_password': {
                'style': {
                    'input_type': 'password'
                }
            }
        }


class ChangePasswordSerializer(Serializer):
    new_password = CharField(max_length=30)

    class Meta:
        extra_kwargs = {
            'new_password': {
                'style': {
                    'input_type': 'password'
                }
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
