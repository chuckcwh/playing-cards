from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from mock import patch, Mock
from cards.models import Player, WarGame
from cards.utils import create_deck, get_random_comic


class ViewTestCase(TestCase):

    def setUp(self):
        create_deck()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn('<h2>Some Random Inspiration</h2>', response.content)

    @patch('cards.utils.requests')
    def test_xkcd(self, mock_request):
        mock_comic = {
            'num': 1433,
            'year': "2014",
            'safe_title': "Lightsaber",
            'alt': "A long time in the future, in a galaxy far, far, away.",
            'transcript': "An unusual gamma-ray burst originating from somewhere across the universe.",
            'img': "http://imgs.xkcd.com/comics/lightsaber.png",
            'title': "Lightsaber",
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_request.get.return_value = mock_response
        self.assertEqual(get_random_comic()['num'], 1433)
        response = self.client.get(reverse('home'))
        self.assertIn('<h3>{} - {}</h3>'.format(mock_comic['safe_title'], mock_comic['year']),
                      response.content)
        self.assertIn('<img alt="{}" src="{}">'.format(mock_comic['alt'], mock_comic['img']),
                      response.content)
        self.assertIn('<p>{}</p>'.format(mock_comic['transcript']), response.content)

    def test_faq(self):
        response = self.client.get(reverse('faq'))
        self.assertIn('<p>Q: Can I win real money on this website?</p>', response.content)

    def test_filters(self):
        response = self.client.get(reverse('filters'))
        self.assertIn('Capitalized Suit: 0 <br>', response.content)
        self.assertIn('Uppercased Rank: TWO', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'tests@tests.com',
            'password1': 'tests',
            'password2': 'tests'
        }
        response = self.client.post(reverse('register'), data)
        self.assertTrue(Player.objects.filter(username=username).exists())
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    # def test_profile(self):
    #     password = 'passsword'
    #     user = Player.objects.create_user(username='tests-user', email='tests@tests.com', password=password)
    #     self.client.login(username=user.username, password=password)
    #     WarGameFactory.create_batch(3, player=user, result=WarGame.WIN)
    #     WarGameFactory.create_batch(2, player=user, result=WarGame.LOSS)
    #     WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
    #     self.assertEqual(Player.get_record_display(), "3-2-4")

    # # not solved
    # def test_login_page(self):
    #     username = 'chuck'
    #     password = '123'
    #     data = {
    #         'username': username,
    #         'password1': password
    #     }
    #     response = self.client.post(reverse('login'), data)
    #     self.assertIsInstance(response, HttpResponseRedirect)
    #     self.assertTrue(response.get('location').endswith(reverse('profile')))

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_profile_page(self):
        password = 'passsword'
        user = Player.objects.create_user(username='tests-user', email='tests@tests.com', password=password)
        self.client.login(username=user.username, password=password)
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertEqual(len(response.context['games']), 2)

    # # not solved
    # def test_war_page(self):
    #     password = 'passsword'
    #     user = Player.objects.create_user(username='tests-user', email='tests@tests.com', password=password)
    #     self.client.login(username=user.username, password=password)
    #
    #     user_card = Card.objects.get(suit='spade', rank='two')
    #     dealer_card = Card.objects.get(suit='spade', rank='three')
    #     self.assertEqual(mail.outbox[0].subject, 'Welcome!')
