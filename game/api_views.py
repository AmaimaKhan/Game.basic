from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

from .models import GameRoom
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ValidationError

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        validate_password(password)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully"}, status=201)

    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({"error": "Internal server error", "details": str(e)}, status=500)



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
