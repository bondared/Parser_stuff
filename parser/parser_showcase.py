import nltk
import sys
import woofst as wf
### ANACONDA PROMPT CODE: "python <scriptname> <firstargument> <secondargument>"

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt")###
path1 = sys.argv[1] # simple_gram.cfg goes here
path2 = sys.argv[2] # probability_gram.pcfg goes here

"""
Uses simple_gram.cfg. Here it is just for clarity's sake:

S -> DP VP
DP -> D NP
NP -> "pirate" | "telescope"
D -> "a" | "the"
VP -> V DP | VP PP
V -> "saw"
PP -> P DP
P -> "with"

Added probability_gram.pcfg with arbitrarily assigned probabilities to check how it would work with the parsers:

S -> DP VP  [1.0]
DP -> D NP  [1.0]
NP -> "pirate"  [0.4]
NP -> "telescope"   [0.4]
NP -> NP PP [0.2]
D -> "a"    [0.5]
D -> "the"  [0.5]
VP -> V DP  [0.7]
VP -> VP PP [0.3]
V -> "saw"  [1.0]
PP -> P DP  [1.0]
P -> "with" [1.0]
"""

response = input("Hello. Shall we begin?\n")
if response.lower() != "yes":
    exit()

# Setting up a trial grammar. Seems to access the files alright.
print("Accessing grammars...") 
grammar1 = nltk.data.load(path1)
grammar2 = nltk.data.load(path2)
print("Found two available grammars:\n 1.Simple CFG\n 2.PCFG\n")
response = input("Please press '1' for CFG or '2' for PCFG.\n")
if response == "1":
    grammar = grammar1
    name = "CFG"
elif response == "2":
    grammar = grammar2
    name = "PCFG"

print("\nYou have chosen " + name + ". Listing the grammar's productions:")
for p in grammar.productions():
    print(p)
 
sentence = input("\nEnter a sentence now:\n").lower().split()

# Now let's try and parse the bitch.
if grammar == grammar2:
    print("\nUsing Viterbi as the default parser")
    v_parser = nltk.ViterbiParser(grammar)
    for tree in v_parser.parse(sentence):
        print(tree)
        # Works fine, but only with PCFGs as it requires probability values.
        # Conversely, non-probabilistic parsers seem to disregard those and work fine with PCFGs as input.
else:
    print("\nUsing Chart as the default parser")
    c_parser = nltk.ChartParser(grammar, trace=2)
    for tree in c_parser.parse(sentence):
        print(tree)
        # NLTK's chart parser working fine.

response = input("\nShould we try a different parser?\n")
if response.lower() != "yes":
    print("Finished.")
    exit()

### WFST ###
print("\nSwitching parsers...")
print("Using WFST...")
wfst = wf.init_wfst(sentence, grammar)
wf.display(wfst, sentence)
print("Showing full grid...")
wfst1 = wf.complete_wfst(wfst, sentence, grammar)
wf.display(wfst1, sentence)

response = input("\nShould we try a different parser?\n")
if response.lower() != "yes":
    print("\nFinished.")
    exit()
# Works fine as well. Will look more into it later.

### SHIFTREDUCE ###
print("\nSwitching parsers...")
print("Using ShiftReduce...")
sr_parser = nltk.ShiftReduceParser(grammar)
for tree in sr_parser.parse(sentence):
    print(tree)
# ShiftReduce seems to provide no output - addressed in the chapter.

response = input("\nShould we try a different parser?\n")
if response.lower() != "yes":
    print("Finished.")
    exit()

### RECURSIVEDESCENT ###
print("\nSwitching parsers...")
print("Using RecursiveDescent...")
rd_parser = nltk.RecursiveDescentParser(grammar)
for tree in rd_parser.parse(sentence):
    print(tree)
# Hmm. Seems to enter an endless loop wherever left-recursion is ivolved, as predicted.

print("Finished.")