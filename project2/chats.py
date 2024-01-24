#
# CSCI 121 Fall 2022
#
# Project 2, Part 2
#
# chats.py
#
# Process a text and distill statistics about the bi-gram and tri-gram
# word occurrences in the entered text. It does this by using a dictionary
# of words and bi-grams. Each dictionary entry gives the list of words
# in the text that follow that word/bi-gram (and possibly a count of the
# number of times each follower does so).
#
# The code then generates random text based on these statistics.
#
#
# Usage: python3 chats.py
#
# This command processes a series of lines of text, looking for
# contiguous runs of alphabetic characters treating them each as a
# word. For each such word, it keeps a count of the number of its
# occurrences in the text.
#
# To end text entry hit RETURN and then CTRL-d.  It then generates
# a random text that tries to mimic the text it just processed.
#
#
# Alternative usage: python3 chats.py < textfile.txt
#
# The above instead processes the text of the file in 'textfile.txt'.
#

import sys
import random

STOPPERS   = [".", "!", "?"]
WHITESPACE = [" ","\n","\r","\t"]

def simplifyWord(word):
    """Returns the given string with only certain chars and lowercase.

    This "simplifies" a word so that it only contains a sequence of
    lower case letters and apostrophes, making uppercase letters
    lowercase, and skipping others.  It returns the "simplified" word.
    If, upon simplifying a word, all the characters are skipped, the 
    function returns None.
    
    In normal use, this would convert a word like "Ain't" into the
    word "ain't" and return it. It also would take a text string like
    "it105%s" and give back the string "its".

    This particular function behavior is somewhat arbitrary, written
    to be "good enough" just to handle the spurious other characters
    that might arise in the kinds of free texts from things like
    Project Gutenberg. Sadly, this also strips out accented characters
    and non-Roman alphabetic characters.
    """

    # Scan the word for a-z or ' characters.
    convertedWord = "";
    for c in word:
        if 'A' <= c and  c <= 'Z':
            c = c.lower()
        if ('a' <= c and c <= 'z') or c == '\'':
            convertedWord += c;

    # If we added any such characters, return that word.
    if len(convertedWord) > 0:
        return convertedWord
    else:
        # Otherwise, return None.
        return None

def readWordsFromInput():
    """Returns the contents of console input as a list of words.

    Process the console input as consisting of lines of words. Return
    a list of all the words along with the strings that are "stoppers." 
    Each non-stopper word in the list will be lowercase consisting only
    of the letters 'a'-'z' and also apostrophe. All other characters are
    stripped from the input. Stopper words are specified by the variable
    STOPPERS.
    """
     
    def spacedAround(text,c):
        """Returns modified text with spaces around any occurrence of c.

        Helper function that replaces any string `text` that has the
        character `c` so that all the occurrences of `c` are replaced
        with the substring " c ".
        """
        
        splits = text.split(c)
        return (" "+c+" ").join(splits)

    def spaceInsteadOf(text,c):
        """Returns modified text with space replacing any c.

        Helper function that replaces any string `text` that has the
        character `c` so that all the occurrences of `c` are replaced
        with a space.
        """
        
        splits = text.split(c)
        return (" ").join(splits)
    
    # Read the text into one (big) string.
    textChars = sys.stdin.read()

    # Add spaces around each "stopper" character.
    for stopper in STOPPERS: 
        textChars = spacedAround(textChars,stopper)
        
    # Replace each whitespace character with a space.
    for character in WHITESPACE: 
        textChars = spaceInsteadOf(textChars,character)

    # Split the text according to whitespace.
    rawWords = textChars.split(" ")

    # Process the raw words, simplifying them in the process by
    # skipping any characters that we don't currently handle.
    # We treat the "end of sentence"/"stopper" words specially,
    # including them in the list as their own strings.
    words = []
    for word in rawWords:
        if word not in STOPPERS:
            word = simplifyWord(word)
        if word is not None:
            words.append(word)
    return words


def train(words):
    dict = {}
    #indexing the word list
    index = 0
    #assigning bigrams
    while index < len(words)-1:
        if words[index] not in dict:
            #assigning dictionary keys
            dict[words[index]] = []
        else:
            dict[words[index]].append(words[index+1])
            index += 1
    #assigning trigrams
    index = 0
    while index < len(words)-1:
        if (words[index-1]+' '+words[index]) not in dict:
            dict[words[index-1]+' '+words[index]] = []
        else:
            dict[words[index-1]+' '+words[index]].append(words[index+1])
            index += 1
    return dict

def chat(biTriDict,numLines,lineWidth):
    """ My comments are mostly in the code itself. Essentially, this just reads the biTriDict and creates 
    a random string from there. There are a couple features in the code that help clean up the resultant string."""
    #creating the empty list
    box = ''
    lineCounter = 1
    #creating the variables prev1 and prev2 that store the last choice of the string
    prev2 = random.choice(biTriDict['.'])
    box += ' '+prev2
    prev1 = random.choice(biTriDict['. '+prev2])
    box += ' '+prev1
    #creating the variable currentLineLength that will dictate when to make a new line
    currentLineLength = len(prev2+prev1)+2
    while lineCounter <= numLines:
        #adding the new lines
        if currentLineLength > lineWidth and lineCounter != numLines:
            box += ' \n'
            currentLineLength = 0
            lineCounter += 1
        elif currentLineLength > lineWidth and lineCounter == numLines:
            lineCounter += 1
        a = prev2+' '+prev1
        if lineCounter <= numLines:
            if a not in biTriDict:
                #if the combination of the last two choices aren't in the dictionary:
                if prev1 in biTriDict:
                    #choose a random variable from the previous variable's bigram
                    b = random.choice(biTriDict[prev1])
                    box += ' '+b
                    prev2 = prev1
                    prev1 = b
                    currentLineLength += len(b)+1
                else:
                    #otherwise, choose a random variable from the '.' bigram
                    b = random.choice(biTriDict['.'])
                    box += ' '+b
                    prev2 = prev1
                    prev1 = b
                    currentLineLength += len(b)+1
            #choose a random variable in the last two choices' trigram
            else:
                b = random.choice(biTriDict[a])
                box += ' '+b
                prev2 = prev1
                prev1 = b
                currentLineLength += len(b)+1
    if box[len(box)-1] not in STOPPERS:
        box += ' '+random.choice(STOPPERS)
    lindex = 0
    while lindex < len(box):
        #removing whitespace around stoppers
        if box[lindex] in STOPPERS:
            firstHalf = box[:lindex-1]
            secondHalf = box[lindex:]
            box = firstHalf+secondHalf
        lindex += 1
    box = box.split(' ')
    windex = 0
    while windex < len(box):
        #removing weird floating stoppers after line endings
        if box[windex] == '\n.' or box[windex] == '\n!' or box[windex] == '\n?':
            box[windex] = random.choice(STOPPERS)
            box[windex-1] += box[windex]
            box.remove(box[windex])
            box.insert(windex, '\n')
        windex += 1
    box = ' '.join(box)
    print(box)


#
# The main script. This script does the following:
#
# * Processes a series of lines of text input into the console.
#      => The words of the text are put in the list `textWords`
#
# * Scans the text to compute statistics about bi-grams and tri-
# grams that occur in the text. This uses the function `train`.
#
# • Generates a random text from the bi-/tri-gram dictionary
#   using a stochastic process. This uses the procedure 'chat'.
#

if __name__ == "__main__":

    # Read the words of a text (including ".", "!", and "?") into a list.
    print("READING text from STDIN. Hit ctrl-d when done entering text.")
    textWords = readWordsFromInput()
    print("DONE.")

    # Process the words, computing a dictionary.
    biTriDict = train(textWords)
    chat(biTriDict, 30, 70)
