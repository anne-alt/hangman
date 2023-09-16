from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.urls import path
from random import choice
from .models import HangmanApi
from .serializers import HangmanApiSerializer

# API Views using DRF
class NewGameView(generics.CreateAPIView):
    queryset = HangmanApi.objects.all()
    serializer_class = HangmanApiSerializer

    def create(self, request, *args, **kwargs):
        # Choose a random word from the list of words
        word_to_guess = choice(HangmanApi.WORDS)

        # Initialize the game state
        game = HangmanApi(
            word_to_guess=word_to_guess,
            current_word_state='_' * len(word_to_guess),
            incorrect_guesses=0,
            max_incorrect_guesses=len(word_to_guess) // 2,  # Half the length of the word
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

class GuessView(generics.UpdateAPIView):
    queryset = HangmanApi.objects.all()
    serializer_class = HangmanApiSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        guessed_letter = request.data.get('guessed_letter')

        # Check if the game is still in progress
        if game.game_state == 'InProgress':
            # Check if the guessed letter is in the word to guess
            if guessed_letter in game.word_to_guess:
                # Update the current word state with the correct guess
                new_word_state = ''
                for i in range(len(game.word_to_guess)):
                    if game.word_to_guess[i] == guessed_letter:
                        new_word_state += guessed_letter
                    else:
                        new_word_state += game.current_word_state[i]
                game.current_word_state = new_word_state
                # Check for game over condition (won)
                if game.current_word_state == game.word_to_guess:
                    game.game_state = 'Won'
            else:
                # Increment the count of incorrect guesses
                game.incorrect_guesses += 1
                # Check for game over condition (lost)
                if game.incorrect_guesses >= game.max_incorrect_guesses:
                    game.game_state = 'Lost'

            # Save the updated game state
            game.save()

            # Create a response dictionary
            response_data = {
                "game_state": game.game_state,
            }

            if game.game_state == 'InProgress':
                response_data["current_word_state"] = game.current_word_state
                response_data["incorrect_guesses"] = game.incorrect_guesses
                response_data["max_incorrect_guesses"] = game.max_incorrect_guesses

            return Response(response_data)
        else:
            # Return a response indicating that the game is already over
            return Response({"message": "The game is already over."}, status=status.HTTP_400_BAD_REQUEST)
