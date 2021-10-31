import factory

from strategy.models import Strategy, StrategySharing, UserStrategy


class UserStrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserStrategy


class StrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Strategy


class StrategySharingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StrategySharing
