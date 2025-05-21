from django.shortcuts import render

import random
from django.shortcuts import render, redirect
from .models import Score

deck = list(range(2, 15))  # 2-14, where 11=J, 12=Q, 13=K, 14=A

def index(request):
    first_card = random.choice(deck)
    request.session['current_card'] = first_card
    return render(request, 'game/index.html', {'card': first_card})

def play(request):
    guess = request.GET.get('guess')
    current_card = request.session.get('current_card', random.choice(deck))
    wrong_guesses = request.session.get('wrong_guesses', 0)
    score = request.session.get('score', 0)

    next_card = random.choice(deck)
    result = ''

    if guess:
        if guess == 'higher' and next_card > current_card:
            result = 'You guessed right!'
            score += 1
        elif guess == 'lower' and next_card < current_card:
            result = 'You guessed right!'
            score += 1
        else:
            result = 'You guessed wrong!'
            wrong_guesses += 1

    game_over = wrong_guesses >= 3

    if game_over:
        Score.objects.create(
            player_name='Guest',  # Replace with request.user.username if using auth
            score=score
        )
        # Reset game state for a new game
        request.session['wrong_guesses'] = 0
        request.session['score'] = 0
        result += " Game over! Your score has been saved."
    else:
        request.session['wrong_guesses'] = wrong_guesses
        request.session['score'] = score

    request.session['current_card'] = next_card

    return render(request, 'game/results.html', {
        'current_card': current_card,
        'next_card': next_card,
        'result': result,
    })

def play_again(request):
    # Reset session variables
    request.session.flush()  # clears all session data
    return redirect('index')

def leaderboard(request):
    top_scores = Score.objects.order_by('-score')[:10]
    return render(request, 'game/leaderboard.html', {'top_scores': top_scores})
