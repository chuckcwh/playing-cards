from django.test import TestCase
from cards.models import Card, WarGame, Player
from cards.tests.factories import WarGameFactory


class ModelTestCase(TestCase):
    def test_get_ranking(self):
        card = Card.objects.create(suit=Card.CLUB, rank='jack')
        self.assertEqual(card.get_ranking(), 11)

    def test_get_war_result(self):
        card = Card.objects.create(suit=Card.CLUB, rank='jack')
        card_to_check = Card.objects.create(suit=Card.CLUB, rank='three')
        self.assertEqual(card.get_war_result(card_to_check), 1)

        card_to_check2 = Card.objects.create(suit=Card.CLUB, rank='king')
        self.assertEqual(card.get_war_result(card_to_check2), -1)

        card_to_check3 = Card.objects.create(suit=Card.CLUB, rank='jack')
        self.assertEqual(card.get_war_result(card_to_check3), 0)

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_wins(self):
        user = Player.objects.create_user(username='tests-user', email='tests@tests.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)

    def test_get_losses(self):
        user = Player.objects.create_user(username='tests-user', email='tests@tests.com', password='password')
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)

    def test_get_ties(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_ties(), 4)

    def test_get_record_display(self):
        user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_record_display(), "2-3-4")
