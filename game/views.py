import random
from django.shortcuts import render, redirect
from .models import Score

from django.contrib.auth.forms import UserCreationForm

def game_over(request):
    score = request.session.get('score', 0)
    return render(request, 'game/game_over.html', {'score': score})

deck = list(range(2, 15))  # 2–14, where 11=J, 12=Q, 13=K, 14=A

def index(request):
    # Start new game
    request.session['score'] = 0
    request.session['wrong_guesses'] = 0
    request.session['current_card'] = random.choice(deck)
    return render(request, 'game/index.html', {'card': request.session['current_card']})

def play(request):
    if request.method != 'POST':
        return redirect('index')  # prevent GET access

    guess = request.POST.get('guess')
    current_card = request.session.get('current_card')
    score = request.session.get('score', 0)
    wrong_guesses = request.session.get('wrong_guesses', 0)

    next_card = random.choice(deck)
    result = ''

    if guess == 'higher' and next_card > current_card:
        result = 'You guessed right!'
        score += 1
    elif guess == 'lower' and next_card < current_card:
        result = 'You guessed right!'
        score += 1
    else:
        result = 'You guessed wrong!'
        wrong_guesses += 1

    # Update session
    request.session['score'] = score
    request.session['wrong_guesses'] = wrong_guesses
    request.session['current_card'] = next_card

    # Game Over condition
    if wrong_guesses >= 3:
        # Save score
        Score.objects.create(player_name='Guest', score=score)
        return redirect('game_over')

    return render(request, 'game/results.html', {
        'result': result,
        'current_card': current_card,
        'next_card': next_card,
        'score': score,
        'wrong_guesses': wrong_guesses,
    })

def game_over(request):
    score = request.session.get('score', 0)
    return render(request, 'game/game_over.html', {'score': score})

def play_again(request):
    request.session.flush()
    return redirect('index')

def leaderboard(request):
    top_scores = Score.objects.order_by('-score')[:10]
    return render(request, 'game/leaderboard.html', {'top_scores': top_scores})
