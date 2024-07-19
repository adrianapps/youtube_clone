import factory
from factory.django import DjangoModelFactory
from channel.models import User, Channel


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User


class ChannelFactory(DjangoModelFactory):
    name = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    description = factory.Faker("text")

    class Meta:
        model = Channel
