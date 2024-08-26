import factory
from factory.django import DjangoModelFactory, FileField, ImageField
from channel.tests.factories import UserFactory, ChannelFactory
from video.models import Tag, Video, WatchLater, Comment


class TagFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Tag


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    channel = factory.SubFactory(ChannelFactory)
    file = FileField(filename='example.mp4')
    thumbnail = ImageField()
    description = factory.Faker('text')
    views = factory.Faker("random_int", min=0, max=100000)

    @factory.post_generation
    def tag(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tag.add(tag)

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for like in extracted:
                self.likes.add(like)

    @factory.post_generation
    def dislikes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for dislike in extracted:
                self.dislikes.add(dislike)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    video = factory.SubFactory(VideoFactory)
    user = factory.SubFactory(UserFactory)
    content = factory.Faker("text")


class WatchLaterFactory(DjangoModelFactory):
    class Meta:
        model = WatchLater

    video = factory.SubFactory(VideoFactory)
    user = factory.SubFactory(UserFactory)
