import factory

from strategy.models import UserStrategy, Strategy


class UserStrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserStrategy


class StrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Strategy
