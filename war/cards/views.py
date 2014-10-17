import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from cards.forms import EmailUserCreationForm
from cards.models import Card, WarGame
from cards.utils import get_random_comic


def home(request):
    return render(request, 'cards.html', {
        'comic': get_random_comic()
    })


def filters(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_filters.html', data)


def template_tags(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_template_tags.html', data)


def first_filter(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'first_filter.html', data)


def suit_filter(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_suits.html', data)


@login_required
def profile(request):
    return render(request, 'profile.html',
                  {
        'games': WarGame.objects.filter(player=request.user),
        'wins': request.user.get_wins(),
        'losses': request.user.get_losses()
    })


def faq(request):
    return render(request, 'faq.html', {})


def blackjack(request):
    data = {
        'cards': Card.objects.order_by('?')[:2]
    }

    return render(request, 'blackjack.html', data)


def poker(request):
    data = {
        'cards': Card.objects.order_by('?')[:5]
    }

    return render(request, 'poker.html', data)


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


@login_required()
def war(request):
    cards = list(Card.objects.order_by('?'))
    user_card = cards[0]
    dealer_card = cards[1]

    result = user_card.get_war_result(dealer_card)
    WarGame.objects.create(result=result, player=request.user)

    return render(request, 'war.html', {
        'user_cards': [user_card],
        'dealer_cards': [dealer_card],
        'result': result
    })


@login_required()
def war_all(request):
    return render(request, "war_all.html")


# ajax
@csrf_exempt
def war_all_draw(request):
    cards = Card.objects.order_by('?')
    # b = serializers.serialize('json', [cards])
    # print b
    collection = []
    for card in cards:
        a = serializers.serialize('json', [card])
        collection.append(a)
    user_card_deck = collection[0:26]
    dealer_card_deck = collection[26:52]
    data = [user_card_deck, dealer_card_deck]
    return HttpResponse(json.dumps(data),
        content_type='application/json')
