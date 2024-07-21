from rest_framework import serializers

from channel.models import User
from channel.models import Channel


class UserPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChannelListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Channel
        fields = [
            'id',
            'name',
            'user',
            'description',
            'creation_date',
            'avatar',
        ]


class ChannelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'id',
            'name',
            'user',
            'description',
            'subscribers',
            'creation_date',
            'avatar',
        ]
