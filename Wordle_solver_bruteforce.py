import requests

BASE_URL = "https://wordle.votee.dev:8000"

def get_feedback_from_api(word):
    # Send a GET request to the API with the word as a guess
    response = requests.get(f"{BASE_URL}/word/{word}", params={'guess': word})
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        return response.json()  # Assuming the response is in JSON format
    else:
        print(f"Error with word {word}: {response.status_code}")
        return None

def check_wordlist(file_path):
    # Read the words from the wordlist file
    with open(r"C:\Users\User\Desktop\worlde_api\wordle_answers.txt", 'r') as file:
        wordlist = [line.strip() for line in file.readlines()]

    # Iterate through the wordlist and check each word
    for word in wordlist:
        feedback = get_feedback_from_api(word)
        
        if feedback:
            # Check if all letters are marked as "correct"
            if all(letter['result'] == 'correct' for letter in feedback):
                print(f"The correct word is: {word}")
                return word

    print("No correct word found in the list.")
    return None

# Example usage:
wordlist_file_path = 'wordlist.txt'  # Replace with your actual file path
correct_word = check_wordlist(wordlist_file_path)

if correct_word:
    print(f"The correct word is: {correct_word}")
else:
    print("No correct word found.")
