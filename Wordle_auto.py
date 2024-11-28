import requests
import logging
import sys
from collections import Counter

BASE_URL = "https://wordle.votee.dev:8000"



# Load a wordlist of valid 5-letter words
with open("wordle_answers.txt") as f:
    wordlist = [word.strip() for word in f if len(word.strip()) == 5]

def play_random_word():
    size = 5  # Word length
    seed = None  # Optional seed

    # Initialize state
    correct_letters = [""] * size  # Letters in the correct positions
    present_letters = set()  # Letters in the word but misplaced
    absent_letters = set()  # Letters not in the word

    guess = "abate"  # Start with a random guess
    global wordlist

    while True:
        # Make a guess
        response = requests.get(
            f"{BASE_URL}/random",
            params={"guess": guess, "size": size, "seed": seed}
        )
        feedback = response.json()

        print(f"Guess: {guess} | Feedback: {feedback}")

        # Check if solved
        if all(item["result"] == "correct" for item in feedback):
            print(f"Solved! The word is: {guess}")
            break

        # Update constraints based on feedback
        for item in feedback:
            letter = item["guess"]
            slot = item["slot"]
            result = item["result"]

            if result == "correct":
                correct_letters[slot] = letter
                # Remove letter from present_letters and absent_letters
                present_letters.discard(letter)
                absent_letters.discard(letter)
            elif result == "present":
                if letter not in correct_letters:
                    present_letters.add(letter)
            elif result == "absent" and letter not in correct_letters:
                absent_letters.add(letter)

        # Refine the wordlist dynamically
        wordlist = refine_wordlist(wordlist, correct_letters, present_letters, absent_letters)
        print(f"Refined wordlist: {wordlist[:10]} ({len(wordlist)} words)")

        # Check if valid words are left in the wordlist
        if not wordlist:
            print("No valid words left in the wordlist. Exiting...")
            break

        # Now check all words in the pruned list for validity
        valid_guesses = []
        for word in wordlist:
            valid = True
            for i, letter in enumerate(correct_letters):
                # Ensure correct letters in correct positions
                if letter and word[i] != letter:
                    valid = False
                    break
            if valid:
                # Ensure absent letters are not in the word
                for letter in absent_letters:
                    if letter in word:
                        valid = False
                        break
            if valid:
                # Ensure present letters exist but not in the same position
                for present_letter in present_letters:
                    if present_letter not in word:
                        valid = False
                        break
                    if word.find(present_letter) == correct_letters.index(''):
                        valid = False
                        break

            if valid:
                valid_guesses.append(word)

        if valid_guesses:
            guess = valid_guesses[0]  # Pick the first valid word
        else:
            print("No valid words left. Exiting...")
            break

def refine_wordlist(wordlist, correct_letters, present_letters, absent_letters):
    size = len(correct_letters)
    refined_wordlist = []

    for word in wordlist:
        valid = True
        
        # Check correct letters first (position-based)
        for i, letter in enumerate(correct_letters):
            if letter and word[i] != letter:
                valid = False
                break

        # Check absent letters (should not appear at all)
        if valid:
            for letter in absent_letters:
                if letter in word:
                    valid = False
                    break

        # Check present letters (must appear but not in the same position)
        if valid:
            for present_letter in present_letters:
                if present_letter in word:
                    present_index = word.find(present_letter)
                    # Ensure present letters are not in the same position as previously guessed
                    if present_index != -1 and word[present_index] == present_letter:
                        valid = False
                        break
                else:
                    valid = False
                    break
        
        if valid:
            refined_wordlist.append(word)

    return refined_wordlist










play_random_word()
