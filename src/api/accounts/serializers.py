from rest_framework.serializers import ModelSerializer, CharField, Serializer, DateField, ChoiceField
from accounts.models import User
from profiles.models import Profile


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
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40, allow_blank=True)
    gender = ChoiceField(choices=GENDER)
    date_of_birth = DateField()

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'alias': instance.alias,
            'email': instance.email,
            'is_verified': instance.is_verified
        }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'gender', 'date_of_birth')
        extra_kwargs = {
            'password': {
                'style': {
                    'input_type': 'password'
                }
            },
        }

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        gender = validated_data.pop('gender')
        date_of_birth = validated_data.pop('date_of_birth')
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile(user=user, first_name=first_name, last_name=last_name, gender=gender,
                          date_of_birth=date_of_birth)
        profile.save()
        return user
