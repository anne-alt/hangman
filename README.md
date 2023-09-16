# Hangman API

**Hangman API** is a simple Django REST Framework (DRF) application that allows users to play the classic word-guessing game, Hangman. This README provides detailed instructions on how to set up the application, how to use the API endpoints, and how to run tests.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Create a New Game](#create-a-new-game)
  - [Get Game State](#get-game-state)
  - [Make a Guess](#make-a-guess)
  - [Get the Number of Games in Progress](#get-the-number-of-games-in-progress)
  - [Get All Games (Won, Lost, and In Progress)](#get-all-games-won-lost-and-in-progress)
- [Running Tests](#running-tests)

## Installation

Follow these steps to set up the Hangman API on your local machine:

1. **Clone the Repository**:

    ```bash
    git clone <repository_url>
    cd hangman-api
    ```

2. **Create a Virtual Environment** (Optional but recommended):

    ```bash
    python -m venv venv
    source env/bin/activate  # On Windows, use: env\Scripts\activate
    ```

3. **Install Dependencies**:

    - pip install django
    - pip install djangorestframework

4. **Apply Migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Run the Development Server**:

    ```bash
    python manage.py runserver
    ```

The API should now be accessible at `http://localhost:8000/`.

## API Endpoints

### Create a New Game

- **Endpoint:** `/game/new/`
- **HTTP Method:** POST

Create a new Hangman game by sending a POST request to this endpoint. A random word will be selected from a predefined list, and the game will be initialized with the following default settings:

- `word_to_guess`: The randomly selected word.
- `current_word_state`: A string of underscores, representing the current state of the word.
- `incorrect_guesses`: The number of incorrect guesses (initially set to 0).
- `max_incorrect_guesses`: Half the length of the word (rounded up).
- `game_state`: 'InProgress' to indicate that the game has started.

Example Request:

```bash
curl -X POST http://localhost:8000/game/new
```

Example Response:
```json
{
    "id": 1,
    "word_to_guess": "Hangman",
    "current_word_state": "_______",
    "incorrect_guesses": 0,
    "max_incorrect_guesses": 4,
    "game_state": "InProgress"
}
```
### Get Game State

- **Endpoint:**  `/game/{game_id}`
- **HTTP Method:** GET

Retrieve the current state of a game by providing its `game_id` in the URL.

Example Request:
```bash
curl http://localhost:8000/game/1/
```

Example Response:
```json
{
    "id": 1,
    "word_to_guess": "Hangman",
    "current_word_state": "H___m___",
    "incorrect_guesses": 2,
    "max_incorrect_guesses": 4,
    "game_state": "InProgress"
}
```

### Make a Guess

- **Endpoint:**  `/game/{game_id}/guess`
- **HTTP Method:** PATCH

Make a guess for the Hangman game specified by `game_id`. Provide the guessed letter in the request body as JSON data with the key `guessed_letter`.

Example Request:
```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"guessed_letter": "a"}' http://localhost:8000/game/1/guess
```

Example Response (Correct Guess):
```json
{
    "id": 1,
    "word_to_guess": "Hangman",
    "current_word_state": "H___ma__",
    "incorrect_guesses": 2,
    "max_incorrect_guesses": 4,
    "game_state": "InProgress",
    "correct_guess": true
}
```

Example Response (Incorrect Guess, Game Over):
```json
{
    "id": 1,
    "word_to_guess": "Hangman",
    "current_word_state": "H___ma__",
    "incorrect_guesses": 4,
    "max_incorrect_guesses": 4,
    "game_state": "Lost",
    "correct_guess": false
}
```

### Get the Number of Games in Progress

- **Endpoint:**  `/game/count`
- **HTTP Method:** GET

Retrieve the number of Hangman games that are currently in progress.

Example Request:
```bash
curl http://localhost:8000/game/count
```

Example Response:
```json
{
    "games_in_progress": 2
}
```

### Get All Games (Won, Lost, and In Progress)

- **Endpoint:**  `/game/all`
- **HTTP Method:** GET

Retrieve a list of all Hangman games, including those that are won, lost, and in progress.

Example Request:
```bash
curl http://localhost:8000/game/all
```

Example Response:
```json
[
    {
        "id": 1,
        "word_to_guess": "Hangman",
        "current_word_state": "H___ma__",
        "incorrect_guesses": 4,
        "max_incorrect_guesses": 4,
        "game_state": "Lost"
    },
    {
        "id": 2,
        "word_to_guess": "Python",
        "current_word_state": "P____",
        "incorrect_guesses": 0,
        "max_incorrect_guesses": 3,
        "game_state": "InProgress"
    },
    {
        "id": 3,
        "word_to_guess": "Bottle",
        "current_word_state": "Bottle",
        "incorrect_guesses": 0,
        "max_incorrect_guesses": 3,
        "game_state": "Won"
    }
]
```

## Running Tests

To run the test suite and ensure that the Hangman API is working correctly, follow these steps:

Ensure your virtual environment is activated (if you created one).

Run the tests using the following command:
```bash
python manage.py test
```

You should see the test results, including any failures or errors. This ensures that the application functions as expected.

That's it! You've successfully set up, used, and tested the Hangman API. Enjoy playing Hangman via the API endpoints or use it as a reference for building more complex applications.


















