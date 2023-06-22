# CS1210 Homework2
#
# This file should contain only your own work; there are no partners
# assigned or permitted for Homework assignments.
#
# I certify that the entirety of this file contains only my own work.
# I have not shared the contents of this file with anyone in any form,
# nor have I obtained or included code from any other source aside
# from the code contained in the original homework template file.
from string import punctuation
import matplotlib.pyplot as plt
import re


######################################################################
# Edit the following function definition so it returns a tuple
# containing a single string, your hawkid.
#
# THE AUTOGRADER WILL FAIL TO ASSIGN A GRADE IF YOUR HAWKID IS NOT
# PROPERLY INCLUDED IN THIS FUNCTION. CAVEAT EMPTOR.
######################################################################
def hawkid():
    '''Used by CS1210 Autograder to extract student identity from code.'''
    return(("kvarnr",))

######################################################################
# Some sample regular expressions.
RE = ( ("([sS]han't)","shall not"),        # "shan't" => "shall not"
       ("([wW]on't)","will not"),          # "won't" => "will not"
       ("([cC]an't)","cannot"),            # "can't" => "cannot"
       ("([a-zA-Z])'m\\b","\\1 am"),       # "...'m" => "... am"
       ("([a-zA-Z])'d\\b","\\1 would"),    # "...'d" => "... would"
       ("([a-zA-Z])'s\\b","\\1 is"),       # "...'s" => "... is"
       ("([a-zA-Z])'ll\\b","\\1 will"),    # "...'ll" => "... will"
       ("([a-zA-Z])'ve\\b","\\1 have"),    # "...'ve" => "... have"
       ("([a-zA-Z])'re\\b","\\1 are"),     # "...'re" => "... are"
       ("([a-zA-Z])n't\\b","\\1 not"),     # "...n't" => "... not"
       ("\\bma'a?m\\b", "madam"),          # Abbrevs like Mme.?
       ("\W([a-z])-([a-z])", "\\1\\2"),    # Merge stutters like k-k-kick
       ("-+", " ") )                       # Split words at hyphens.

######################################################################
# readFile(filename, regexes) returns a list of words read from the
# specified file. The second argument is a list of regular expressions
# that should be applied to the text before stripping punctuation from
# the words in the text.
def readFile(file, regexes = RE):
    '''Function opens and reads the file. Then, scans for words in regex
        and substitutes contractions out for their full forms. Finally,
        a tuple is created of every letter in every word and it scans for
        punctuation, and strips it and puts it back together.'''
    file = open(file, 'r') #opens the file into read mode
    words = file.read() #turns the text into a string that can be searched
    for regex in regexes: #scans for contractions
        words = re.sub(str(regex[0]), str(regex[1]), str(words), flags=re.IGNORECASE) #if a contraction is found it is substituted with the regex for the regular word
    L = [''.join(letter for letter in word if letter not in punctuation)for word in words.split()] #every word is split into a tuple of letters, which is then scanned for punctuation, stripped of the punctuation, then joined back together
    return L #returned the list of words without contractions or punctuation
    file.close() #closes the file
    
######################################################################
# findNouns(W, cmin=1) returns a dictionary of proper nouns (as keys)
# and their occurrance counts (as values) provided each key noun
# appears at least cmin times in the text.
def findNouns(W, cmin=1):
    '''Function creates a dictionary and then parses through the text file. While
        parsing the words it checks to see if they are already in the dict. If not
        and the word is a proper noun it is added to the keys of the dict. If
        it is not a proper noun then it is left out. If the word is already in the
        dict then it counts how many times it is used in the text as a value. Then
        it displays the dict of words if the words are greater than the cmin.'''
    x = dict() #assignes an empty dictionary to the variable x
    for i in W: #for every word in the list W
        if i in x: #if word is already in x
            x[i] += 1 #add 1 to the value at that words key
        elif i not in x: #if the word isnt in x
            if i == i.capitalize(): #if the word is capitalized then
                if i.lower() not in W: #if the word lowercased is not in W already
                    x[i] = 1 #set its value equal to 1
        else: #else pass on to the return
            pass
    return{i:x[i] for i in x if x[i] >= cmin} #return a dictionary of the word and how many times it occurs in the text only if it is greater than the cmin

######################################################################
# buildIndex(W, N) returns a dictionary of proper nouns (as keys)
# taken from N and the index value in W for each occurrance of the key
# noun.
def buildIndex(W, N):
    '''Function takes W (the list of words from the text) and N (the dictionary of
        proper nouns and the occurences of these words) and created a dictionary
        with these words as keys and a list of each place the word appears in the
        text'''
    y = dict() #assigns y to an empty dictionary
    for i in range(len(W)): #for word in the range of the length of the word list W
        if W[i] in N.keys() and W[i] not in y.keys(): #if W indexed at i is a key in N and is not already in dictionary y
            y[W[i]] = [i] #A list is created with the word in it
        elif W[i] in y: #if W indexed at i is already in dictionary y
            y[W[i]].append(i) #append the words location to the dictionary at the word
        else: #else passes over the word
            pass
    return y #return dictionary y

######################################################################
# plotChars(N, I, W, xsteps=100) uses matplotlib to plot a character
# plot like the one shown in the handout, where N is a dictionary of
# proper nouns (as returned by findNouns()), I is an index of proper
# nouns and their locations in the text (as returned by buildIndex()),
# W is a list of words in the text (as returned by readFile()) and
# xsteps is the window size within which we count occurrences of each
# character.
def plotChars(N, I, W, xsteps=100):
    '''Function initiates a graph to display mentions of a character in different
        sections of the text'''
    plt.title('Character Map') #sets graph title
    plt.xlabel('Location (Text%)') #set x label of graph
    plt.ylabel('Mentions') #sets y label of graph
    x = list(range(xsteps + 1)) #assigns x to a list of xsteps + 1 so it ranges from 0 to 100 including 100
    Increment = len(W)//xsteps #sets increment of the percentage of text
    for i in N.keys(): #for word in N's keys
        Min = 0 #set min value to 0
        Max = len(W)//xsteps #set max value to 
        y = [0] #sets y to a list 0
        for j in range(xsteps): #for each step in the range of xsteps value
            z = [e for e in I[i] if e >= Min if e < Max] #assigns z to the character names from buildIndex if they are between the min and max restrictions
            Min += Increment #adds the increment to the min
            Max += Increment #adds the increment to the max
            y.append(len(z)) #appends the length of z the list y
        plt.plot(x, y, label = i) #plots the graph with labels using i (the character names)
    plt.legend(loc = 2) #places the legend in the upper left corner of the graph
    plt.show() #show the graph

######################################################################
# plot(file='wind.txt', cmin=100, xsteps=100) is a driver that manages
# the entire analysis and plotting process. It is presented to give
# you an idea of how to use the functions you've just designed.
def plot(file='wind.txt', cmin=100, xsteps=100):
    '''Drive analysis of text contained in file.'''
    W=readFile(file)
    N=findNouns(W, cmin)
    plotChars(N, buildIndex(W, N), W, xsteps)
