from django.shortcuts import render

import random
from django.shortcuts import render, redirect

deck = list(range(2, 15))  # 2-14, where 11=J, 12=Q, 13=K, 14=A

def index(request):
    first_card = random.choice(deck)
    request.session['current_card'] = first_card
    return render(request, 'game/index.html', {'card': first_card})

def play(request):
    guess = request.GET.get('guess')
    current_card = request.session.get('current_card')
    next_card = random.choice(deck)

    result = ''
    if guess == 'higher' and next_card > current_card:
        result = 'You guessed right!'
    elif guess == 'lower' and next_card < current_card:
        result = 'You guessed right!'
    else:
        result = 'You guessed wrong!'

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