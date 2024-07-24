import factory
from factory.django import DjangoModelFactory, ImageField
from channel.models import User, Channel


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class ChannelFactory(DjangoModelFactory):
    class Meta:
        model = Channel
        exclude = ('files',)

    name = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    description = factory.Faker("text")
    avatar = ImageField()
    files = set()

    @factory.post_generation
    def post(self, created, extracted, **kwargs):
        ChannelFactory.files.add(self.avatar)

    @factory.post_generation
    def subscribers(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for subscriber in extracted:
                self.subscribers.add(subscriber)
