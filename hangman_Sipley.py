import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print "Loading word list from file..."
    inFile = open('words.txt', 'r', 0)
    line = inFile.readline()
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    wordlist = loadWords()
    return random.choice(wordlist)

def isWordGuessed(secretWord, guessedWord):
    if secretWord == guessedWord:
        return True

def lettersGuessed(guess, guessedLetters):
    guessedLetters.append(guess)
    return guessedLetters
    
def getGuessedWord(secretWord, guessedLetters):
    guessedWord = ''
    for letter in secretWord:
        if letter in guessedLetters:
            guessedWord += letter
        else:
            guessedWord += '_'          
    return guessedWord             
      
def getAvailableLetters(lettersGuessed): 
    availableLetters = 'abcdefghijklmnopqrstuvwxyz'   
    for letter in lettersGuessed:
        if letter in availableLetters:
            availableLetters = availableLetters.replace(letter,'')
    return availableLetters

def hangman(secretWord):
    guessedLetters = []
    print "Welcome to Hangman, an interactive word guessing game! Can you guess the word I'm thinking of below?  HINT: it contains {} letters.".format(len(secretWord))
    numGuessesLeft = 6  
    while numGuessesLeft > 0:
        
        print getGuessedWord(secretWord, guessedLetters)
        print 'Available letters:',getAvailableLetters(guessedLetters)
        print 'You have {} guesses remaining.'.format(numGuessesLeft)
        guess = raw_input("Choose a letter: ").lower() 
        guessedLetters = lettersGuessed(guess, guessedLetters)    
        if isWordGuessed(secretWord, getGuessedWord(secretWord, guessedLetters)):
            print "\nThe word was '{}'. You guessed it!".format(secretWord)
            break
        elif guess.isalpha() and len(guess) == 1 and guessedLetters.count(guess) == 1:
            if guess in secretWord:
                print "'{}' is in the word!".format(guess)
            else:
                print "'{}' is NOT in the word!".format(guess)
                numGuessesLeft -= 1
        elif guessedLetters.count(guess) > 1:
            print "You've already guessed that!  I guess I won't hold it against you."
        else: 
            print "You can only guess 1 available letter at a time."
        
    if numGuessesLeft == 0:
        print "\nOh no! You've hanged the man! The word was '{}'. Game over.".format(secretWord)
    
secretWord = chooseWord(loadWords)
hangman(secretWord)