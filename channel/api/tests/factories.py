import factory
from factory.django import DjangoModelFactory, ImageField
from channel.models import User, Channel


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    @factory.post_generation
    def set_staff(self, create, extracted, **kwargs):
        if extracted:
            self.is_staff = True
            self.save()

    @factory.post_generation
    def set_superuser(self, create, extracted, **kwargs):
        if extracted:
            self.is_superuser = True
            self.save()


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
    def post(self, create, extracted, **kwargs):
        ChannelFactory.files.add(self.avatar)

    @factory.post_generation
    def subscribers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for subscriber in extracted:
                self.subscribers.add(subscriber)
