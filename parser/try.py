import nltk
import sys
# Make sure to provide both grammars as arguments when running the script:
path1 = sys.argv[1] # trygram.cfg goes here
path2 = sys.argv[2] # probgram.cfg goes here

"""
Uses trygram.cfg. Here it is just for clarity's sake:

S -> DP VP
DP -> D NP
NP -> "pirate" | "telescope"
D -> "a" | "the"
VP -> V DP | VP PP
V -> "saw"
PP -> P DP
P -> "with"

Added probgram.cfg with arbitrarily assigned probabilities to check how it would work with the parsers:

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

# Code taken from Section 4.4, Chapter 8 of the NLTK book
# Would not let me make it a module due to whitespace issues
def init_wfst(tokens, grammar):
    numtokens = len(tokens)
    wfst = [[None for i in range(numtokens+1)] for j in range(numtokens+1)]
    for i in range(numtokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i+1] = productions[0].lhs()
    return wfst

def complete_wfst(wfst, tokens, grammar, trace=False):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    for span in range(2, numtokens+1):
        for start in range(numtokens+1-span):
            end = start + span
            for mid in range(start+1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if nt1 and nt2 and (nt1,nt2) in index:
                    wfst[start][end] = index[(nt1,nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                        (start, nt1, mid, nt2, end, start, index[(nt1,nt2)], end))
    return wfst

def display(wfst, tokens):
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()



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
    c_parser = nltk.ChartParser(grammar)
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
wfst = init_wfst(sentence, grammar)
display(wfst, sentence)
print("Showing full grid...")
wfst1 = complete_wfst(wfst, sentence, grammar)
display(wfst1, sentence)

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