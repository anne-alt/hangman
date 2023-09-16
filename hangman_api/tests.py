from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import HangmanApi
import math  


class NewGameAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_new_game(self):
        response = self.client.post('/game/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HangmanApi.objects.count(), 1)
        game = HangmanApi.objects.first()
        self.assertEqual(game.game_state, 'InProgress')
        self.assertEqual(game.incorrect_guesses, 0)

        # Verify that max_incorrect_guesses is calculated correctly
        expected_max_incorrect_guesses = math.ceil(len(game.word_to_guess) / 2)
        self.assertEqual(game.max_incorrect_guesses, expected_max_incorrect_guesses)

    def test_create_multiple_games(self):
        response = self.client.post('/game/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/game/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HangmanApi.objects.count(), 2)

class GameStateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.game = HangmanApi.objects.create(
            word_to_guess='Pen',
            current_word_state='___',
            incorrect_guesses=1,
            max_incorrect_guesses=2,
            game_state='InProgress'
        )

    def test_get_game_state(self):
        game_id = self.game.id
        response = self.client.get(f'/game/{game_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['game_state'], 'InProgress')
        self.assertEqual(data['current_word_state'], '___')
        self.assertEqual(data['incorrect_guesses'], 1)
        self.assertEqual(data['max_incorrect_guesses'], 2)

    def test_get_game_state_invalid_id(self):
        invalid_id = 999  # Non-existent game ID
        response = self.client.get(f'/game/{invalid_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GuessAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.game = HangmanApi.objects.create(
            word_to_guess='Pen',
            current_word_state='___',
            incorrect_guesses=1,
            max_incorrect_guesses=2,
            game_state='InProgress'
        )

    def test_make_correct_guess(self):
        game_id = self.game.id
        response = self.client.patch(f'/game/{game_id}/guess', {'guessed_letter': 'e'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['game_state'], 'InProgress')
        self.assertEqual(data['correct_guess'], True)
        self.assertEqual(data['current_word_state'], '_e_')
        self.assertEqual(data['incorrect_guesses'], 1)

    def test_make_incorrect_guess(self):
        game_id = self.game.id
        response = self.client.patch(f'/game/{game_id}/guess', {'guessed_letter': 'x'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['game_state'], 'Lost')
        self.assertEqual(data['correct_guess'], False)
        self.assertEqual(data['current_word_state'], '___')
        self.assertEqual(data['incorrect_guesses'], 2)  

    def test_make_guess_invalid_id(self):
        invalid_id = 999  # Non-existent game ID
        response = self.client.post(f'/game/{invalid_id}/guess', {'guessed_letter': 'e'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

