from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

from .models import GameRoom
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

deck = list(range(2, 15))

@api_view(['GET'])
def start_game(request):
    card = random.choice(deck)
    request.session['current_card'] = card
    request.session['score'] = 0
    request.session['wrong_guesses'] = 0
    return Response({'card': card})

@api_view(['POST'])
def guess_card(request):
    guess = request.data.get('guess')
    current = request.session.get('current_card', random.choice(deck))
    score = request.session.get('score', 0)
    wrong = request.session.get('wrong_guesses', 0)

    next_card = random.choice(deck)
    correct = (guess == 'higher' and next_card > current) or (guess == 'lower' and next_card < current)

    if correct:
        score += 1
        result = 'Correct'
    else:
        wrong += 1
        result = 'Incorrect'

    game_over = wrong >= 3
    request.session['current_card'] = next_card
    request.session['score'] = score
    request.session['wrong_guesses'] = wrong

    return Response({
        'result': result,
        'next_card': next_card,
        'score': score,
        'game_over': game_over
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_room(request):
    name = request.data.get('room_name')
    if GameRoom.objects.filter(name=name).exists():
        return Response({'error': 'Room already exists'}, status=400)
    room = GameRoom.objects.create(name=name)
    room.players.add(request.user)
    return Response({'message': 'Room created', 'room': room.name})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_room(request):
    name = request.data.get('room_name')
    try:
        room = GameRoom.objects.get(name=name)
        room.players.add(request.user)
        return Response({'message': 'Joined room', 'room': room.name})
    except GameRoom.DoesNotExist:
        return Response({'error': 'Room does not exist'}, status=404)
