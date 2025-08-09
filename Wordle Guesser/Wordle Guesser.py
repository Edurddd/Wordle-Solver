import random

fileName = "valid-wordle-words.txt" 

with open(fileName, 'r') as file:
    #Load word txt as list
    wordList = file.readlines()
for i, word in enumerate(wordList):
    wordList[i] = word.replace("\n", "")
        
#Create hashmap of every letter, values being a 1x5 array where indecies represent position in word, and 0 = placeholder, x = gray, y= yellow= g = green
letters = {chr(i + 96): [0 for i in range(5)] for i in range(1,27)}
wordsToEliminate = set()
potentialWords = set()
#Checks if words have duplicate letters, for first guess we want to use words with no duplicates
def isUnique(word) -> bool:
    lettersSeen = {chr(i + 96): 0 for i in range(1, 27)}
    for letter in word:
        lettersSeen[letter] += 1
        if lettersSeen[letter] > 1:
            return False
    return True  

firstGuessWords = []

#Iterates through list of words, adds every word with no duplicates to the list of potential first guesses
for word in wordList:
    if isUnique(word):
        firstGuessWords.append(word)

def updateLetters(guess):
    for pos, letter in enumerate(guess):
        if letters[letter][pos] == 0:
            letters[letter][pos] = input(f"What color was {letter}? Enter 'x' for grey, 'y' for yellow, or 'g' for green ")
    
def elimateWords():
    wordsToEliminate.clear()
    #gray logic
        #Must check how many times the letter has shown up in different positions 
        #If the letter is always grey remove all words that have the letter
        #If the letter has cases where it isn't grey only get rid of words that have the letter in positions where it is grey
    for letter in letters:
        grayApperances = 0
        letterApperances = 0
        for pos in range(5):
            if letters[letter][pos] == 'x':
                grayApperances += 1
            if letters[letter][pos] != 0:
                letterApperances += 1
        if grayApperances == letterApperances and letterApperances > 0:
           for word in wordList:
               if letter in word:
                   wordsToEliminate.add(word)
        elif grayApperances != letterApperances and grayApperances > 0:
            for pos in range(5):
                if letters[letter][pos] =='x':
                    for word in wordList:
                        if word[pos] == letter:
                            wordsToEliminate.add(word)
                    
    #yellow logic
    #If a letter is yellow in a position get rid of all words with the letter in that position and eliminate words that don't have the letter at all
    for letter in letters:
       for pos in range(5):
           if letters[letter][pos] == 'y':
               for word in wordList:
                   if word[pos] == letter:
                       wordsToEliminate.add(word)
                   elif letter not in word:
                        wordsToEliminate.add(word)    
    #green logic 
    #if a letter is green in a position eliminate all words that don't include that letter in that position 
    for letter in letters:
        for pos in range(5):
            if letters[letter][pos] == 'g':
                for word in wordList:
                    if word[pos] != letter:
                        wordsToEliminate.add(word)
    for word in wordsToEliminate:
        wordList.remove(word)
      
for turn in range(6):
    if turn == 0:
        guess = random.choice(firstGuessWords)
        print(f"Try: {guess}")
        updateLetters(guess)
        elimateWords()
    else:
        if len(wordList) == 1:
            print(f'The word is: {wordList[0]} \ntoo ez')
            break
        elif len(wordList) > 1:
            guess = random.choice(wordList)
            print(f"Try: {guess}")
            updateLetters(guess)

            elimateWords()
