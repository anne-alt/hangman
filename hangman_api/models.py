from django.db import models
import math 

class HangmanApi(models.Model):
    WORDS = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]
    word_to_guess = models.CharField(max_length=100)
    current_word_state = models.CharField(max_length=100)
    incorrect_guesses = models.PositiveIntegerField(default=0)
    max_incorrect_guesses = models.PositiveIntegerField(default=0)  # Default to 0 initially
    game_state = models.CharField(max_length=20, default="InProgress")

    def save(self, *args, **kwargs):
        # Calculate max_incorrect_guesses based on the length of word_to_guess
        self.max_incorrect_guesses = math.ceil(len(self.word_to_guess) / 2)
        super().save(*args, **kwargs)
