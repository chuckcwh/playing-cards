import factory
from cards.models import WarGame


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'
    result = WarGame.TIE


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.Player'
    username = factory.Sequence(lambda i: 'User%d' % i)
    email = factory.lazy_attribute(lambda o: '%s@gmail.com' % o.username)
