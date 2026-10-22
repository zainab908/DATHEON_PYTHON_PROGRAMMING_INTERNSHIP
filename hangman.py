import random

#step 1 : Load the english word list.
with open("words.txt","r",encoding="utf-8") as file:
    words=[
        line.strip().lower()
        for line in file
        if line.strip().isalpha()
    ]

if not words:
    print("No valid words found in words.txt")
    raise SystemExit

#step 2 : Select a random secret word.

secret_word=random.choice(words)

#step 3 : Create variables for the game.

guessed_letters= set()
attempts_left=6

#step 4 : Create the hangman drawings!

hangman_stages=[
    """
     +---+
         |
         |
         |
        ===
   """   ,
   """
    +---+
    O   |
        |
        |
       ===
   """  ,
   """
   +---+
   O   |
   |   |
       | 
      === 
   """ ,
   """
   +---+
   O   |
  /|   |
       | 
      === 
   """ ,
   """
   +---+
   O   |
  /|\\  |
       |
      ===
   """ , 
   """
   +---+
   O   |
  /|\\  |
  /    |
      ===
   """  ,
   """
   +---+
   O   |
  /|\\  |
  / \\  |
      ===  
   """       
]

print("Welcome to Hangman!")
print("Guess the hidden word , one at a time.")
print("You have 6 incorrect guesses available.")

#step 5 : Main game loop.

while attempts_left>0:

    # Displays the current hangman drawing.
    print(hangman_stages[6-attempts_left])

    #Displays the hidden word.
    display_word=""

    for letter in secret_word:
        if letter in guessed_letters:
            display_word=display_word + letter

        else:
            display_word=display_word + "_"    

    print("\nword:"," ".join(display_word))  
    print("Incorrect guesses left:", attempts_left)  

    if guessed_letters:
        print("Guessed letters:"," ".join(sorted(guessed_letters)))    

    else:
        print("Guessed letters: None") 

    # Check whether the player has won. 
    if all(letter in guessed_letters for letter in secret_word):
        print("\nCongratulations! you guessed the word !")  
        print("The word was:", secret_word)     
        break

    # Ask for a letter.
    guess=input("\nGuess a letter:").lower().strip()

    #Validate the input.
    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input . Enter one letter only.")
        continue

    #Prevent duplicate guesses.
    if guess in guessed_letters:
        print("You already guessed that letter. Try another.")
        continue

    #Store the new guess.
    guessed_letters.add(guess)

    #Check the guess.
    if guess in secret_word:
        print("Correct guess.")

    else:
        attempts_left= attempts_left-1
        print("Incorrect guess!")   

#step 6: Display the final result.
if attempts_left == 0:
    print(hangman_stages[6])         
    print("\nGame over! you ran out of attempts.")
    print("The correct word was:",secret_word)