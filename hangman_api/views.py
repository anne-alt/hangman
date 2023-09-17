from django.shortcuts import render
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.urls import path
from random import choice
from .models import HangmanApi
from .serializers import HangmanApiSerializer, GuessSerializer

# API Views using DRF

class AllGamesView(generics.ListAPIView):
    serializer_class = HangmanApiSerializer

    def get_queryset(self):
        # Retrieve games with different states
        queryset = HangmanApi.objects.all()
        return queryset

class InProgressGamesCountView(APIView):
    def get(self, request):
        # Count the number of games in progress
        games_in_progress = HangmanApi.objects.filter(game_state='InProgress').count()

        return Response({"games_in_progress": games_in_progress})


class NewGameView(generics.CreateAPIView):
    queryset = HangmanApi.objects.all()
    serializer_class = HangmanApiSerializer

    def create(self, request, *args, **kwargs):
        # Choose a random word from the list of words
        word_to_guess = choice(HangmanApi.WORDS)

        max_incorrect_guesses = math.ceil(len(word_to_guess) / 2)


        # Initialize the game state
        game = HangmanApi(
            word_to_guess=word_to_guess,
            current_word_state='_' * len(word_to_guess),
            incorrect_guesses=0,
            max_incorrect_guesses=max_incorrect_guesses,            
            game_state='InProgress'
        )

        # Save the game state
        game.save()

        serializer = self.get_serializer(game)
        return Response(serializer.data)

class GameStateView(generics.RetrieveAPIView):
    queryset = HangmanApi.objects.all()
    serializer_class = HangmanApiSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        game = self.get_object()
        remaining_incorrect_guesses = game.max_incorrect_guesses - game.incorrect_guesses

        serializer = self.get_serializer(game)
        data = serializer.data
        data['remaining_incorrect_guesses'] = remaining_incorrect_guesses

        return Response(data)


class GuessView(generics.UpdateAPIView):
    queryset = HangmanApi.objects.all()
    serializer_class = HangmanApiSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        
        # Use the GuessSerializer for validating guessed_letter
        serializer = GuessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guessed_letter = serializer.validated_data['guessed_letter'].lower()  # Convert to lowercase

        # Convert the word to guess to lowercase for case-insensitive comparison
        word_to_guess_lower = game.word_to_guess.lower()

        # Check if the game is still in progress
        if game.game_state == 'InProgress':
            # Check if the guessed letter is in the word to guess (case-insensitive)
            if guessed_letter in word_to_guess_lower:
                # Update the current word state with the correct guess
                new_word_state = ''
                for i in range(len(game.word_to_guess)):
                    if word_to_guess_lower[i] == guessed_letter:
                        new_word_state += game.word_to_guess[i]  # Use the original casing
                    else:
                        new_word_state += game.current_word_state[i]
                game.current_word_state = new_word_state
                # Check for game over condition (won)
                if game.current_word_state == game.word_to_guess:
                    game.game_state = 'Won'
                correct_guess = True  # Guess was correct
            else:
                # Increment the count of incorrect guesses
                game.incorrect_guesses += 1
                # Check for game over condition (lost)
                if game.incorrect_guesses >= game.max_incorrect_guesses:
                    game.game_state = 'Lost'
                    game.incorrect_guesses = game.max_incorrect_guesses  # Set to max allowed
                correct_guess = False  # Guess was incorrect

            # Save the updated game state
            game.save()

            # Create a response dictionary
            response_data = {
                "game_state": game.game_state,
                "correct_guess": correct_guess,  # Include correct_guess field
                "current_word_state": game.current_word_state,  # Always include current_word_state
                "incorrect_guesses": game.incorrect_guesses,  # Include incorrect_guesses field
            }

            if game.game_state == 'InProgress':
                response_data["max_incorrect_guesses"] = game.max_incorrect_guesses

            return Response(response_data)
        else:
            # Return a response indicating that the game is already over
            return Response({"message": "The game is already over."}, status=status.HTTP_400_BAD_REQUEST)