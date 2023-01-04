import re
import random
from tkinter import ttk
from tkinter import *
root = Tk()
root.title('Hangman?')
root.minsize(400,300)
titleScreen = Frame(master=root)
titleScreen.pack()

dictionary = {}

def generatePatternPermutations(guess, pattern, index, currPermutation):
    list = []
    if index == len(pattern):
        list.append(currPermutation)
        return list
    if pattern[index] == '.':
        list += generatePatternPermutations(guess, pattern, index + 1, currPermutation + '.') +  generatePatternPermutations(guess, pattern, index + 1, currPermutation + guess)  
    else:
        list += generatePatternPermutations(guess, pattern, index + 1, currPermutation + pattern[index]) 
    return list

def runGame():
    wordLen = 0
    numLives = 0
    currentPattern = ""
    guesses = []
    wordlist = []

    titleScreen.pack_forget()
    setupScreen = Frame(master = root)
    setupScreen.pack()

    selectedLength = StringVar()
    selectedLength.set("Select Word Length")
    lengthOptions = ttk.Combobox(master=setupScreen, textvariable=selectedLength)
    wordLengths = list(dictionary.keys())
    wordLengths.sort()
    lengthOptions['values'] = wordLengths
    lengthOptions['state'] = 'readonly'
    lengthOptions.pack()
   
    selectedLives = StringVar()
    selectedLives.set("Select Number of Lives")
    livesOptions = ttk.Combobox(master=setupScreen, textvariable=selectedLives)
    livesOptions['values'] = list(range(1,27))
    livesOptions['state'] = 'readonly'
    livesOptions.pack()

    gameScreen = Frame(master = root)
    guessFrame = Frame(master=gameScreen)
    livesText= StringVar()
    livesLabel = Label(master=gameScreen, textvariable=livesText)
    currentWordText = StringVar()
    currentWordLabel = Label(master= gameScreen,textvariable=currentWordText, height = 3)
    previousGuessesText = StringVar()
    previousGuessesText.set("Guesses: ")
    previousGuessesLabel = Label(master=gameScreen,textvariable=previousGuessesText)
    selectedGuess = StringVar()
    guessOptions = ttk.Combobox(master=guessFrame, textvariable=selectedGuess, width=3)
    guessOptions['values'] = [chr(i) for i in range(65,91)]
    guessOptions['state'] = 'readonly'
    def guessCommand():
        nonlocal numLives
        nonlocal wordlist
        nonlocal currentPattern
        options = list(guessOptions['values'])
        options.remove(selectedGuess.get())
        guessOptions['values'] = options
        guessButton['state'] = DISABLED
        guesses.append(selectedGuess.get().lower())
        guesses.sort()
        previousGuessesString = "Guesses: "
        for g in guesses:
            previousGuessesString += g.upper() + " "
        previousGuessesString = previousGuessesString[0:-1]
        previousGuessesText.set(previousGuessesString)
        resultsTuple = processGuess(selectedGuess.get().lower(), currentPattern, wordlist, guesses)
        if(currentPattern == resultsTuple[0]):
            numLives-=1
            livesText.set("Lives Remaining: " + str(numLives))
            guessResultText.set("Incorrect Guess")
        else:
            guessResultText.set("Correct Guess")
        wordlist = resultsTuple[1]
        currentPattern = resultsTuple[0]
        newPatternRepresentation = ""
        for char in currentPattern:
            if char == ".":
                newPatternRepresentation += "_ "
            else:
                newPatternRepresentation += char.upper() + " "
        newPatternRepresentation = newPatternRepresentation[:-1]
        currentWordText.set(newPatternRepresentation)
        selectedGuess.set("")
        if(numLives < 1):
            guessOptions['state'] = DISABLED
            finalResultText.set("You Lose! Word was: " + random.choice(wordlist).upper())
            finishButton.grid(row=6)
        if("." not in currentPattern):
            guessOptions['state'] = DISABLED
            finishButton.grid(row=6)
            finalResultText.set("You Win! Word was: " + wordlist[0].upper())

    guessButton = Button(master=guessFrame, text = "Guess", command=guessCommand)
    guessButton['state'] = DISABLED
    def enableGuess(event):
        guessButton['state'] = NORMAL
    guessOptions.bind('<<ComboboxSelected>>', enableGuess)
    guessOptions.grid(row=0,column=0)
    guessButton.grid(row=0,column=1)
    guessResultText = StringVar()
    guessResultText.set(" ")
    guessResultLabel = Label(master=gameScreen,textvariable=guessResultText)
    finalResultText = StringVar()
    finalResultLabel = Label(master=gameScreen, textvariable=finalResultText)
    finalResultText.set("")
    def finishCommand():
        gameScreen.pack_forget()
        titleScreen.pack()
    finishButton = Button(master=gameScreen,text = "Finish", command=finishCommand)
    currentWordLabel.grid(row = 0)
    livesLabel.grid(row = 1)
    previousGuessesLabel.grid(row = 2)
    guessFrame.grid(row = 3)
    guessResultLabel.grid(row = 4)
    finalResultLabel.grid(row = 5)



    
    def startGame():
        if(selectedLength.get().isnumeric() and selectedLives.get().isnumeric()):
            nonlocal wordLen
            nonlocal numLives
            nonlocal currentPattern
            nonlocal wordlist

            wordLen = int(selectedLength.get())
            numLives = int(selectedLives.get())
            currentPattern = "." * wordLen
            wordlist = dictionary[wordLen]

            currentWordText.set("_ " * (wordLen-1) + "_")
            livesText.set("Lives Remaining: " + str(numLives))
            setupScreen.pack_forget()
            gameScreen.pack()
    
    startButton = Button(master=setupScreen, text="Start Game", command=startGame)
    startButton.pack()

    

    def processGuess(guess, currentPattern, wordlist, guesses):
        patternPermutations = generatePatternPermutations(guess, currentPattern, 0, '')
        resultsDict = {}
        for basePattern in patternPermutations:
            pattern = ''
            if len(guesses) == 0:
                pattern = basePattern
            else:
                for char in basePattern:
                    if char == '.':
                        pattern += '[^'
                        for previousGuess in guesses:
                            pattern+=previousGuess
                        pattern += ']'
                    else:
                        pattern += char
            resultsDict[basePattern] = []
            for word in wordlist:
                if re.match(pattern, word) != None:
                    resultsDict[basePattern].append(word)
        worstResult = patternPermutations[0]
        for basePattern in patternPermutations:
            if len(resultsDict[basePattern]) > len(resultsDict[worstResult]):
                worstResult = basePattern
        wordlist = resultsDict[worstResult]
        currentPattern = worstResult
        return (currentPattern, wordlist)

with open("words.txt") as wordfile:
    for line in wordfile:
        word = line.strip()
        wordLen = len(word)
        if wordLen in dictionary:
            dictionary[wordLen].append(word)
        else:
            dictionary[wordLen] = [word]

title = Label(master=titleScreen, text = "Hangman", height=3)
title.pack()
playButton = Button(master=titleScreen, text="Play Game", command=runGame)
playButton.pack()
previousGameResultText = StringVar()
previousGameResultText.set("")
previousGameResultLabel = Label(master=titleScreen, textvariable=previousGameResultText)
previousGameResultLabel.pack()

root.mainloop()
