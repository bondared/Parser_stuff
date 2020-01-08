import nltk

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
"""

# Code taken from Section 4.4, Chapter 8 of the NLTK book
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

# Setting up a trial grammar. Seems to access the file alright.
print("Accessing grammar...") 
grammar2 = nltk.data.load('file:C:/Users/Dan/Desktop/Parser/parser/trygram.cfg')
for p in grammar2.productions():
    print(p)
 
# Now let's try and parse a bitch.
print("Using Chart as the default parser")
c_parser = nltk.ChartParser(grammar2)
sentence = input("Enter a sentence now:\n").lower().split()
for tree in c_parser.parse(sentence):
    print(tree)
# NLTK's chart parser working fine.

response = input("Should we try a different parser?\n")
if response.lower() != "yes":
    print("Finished.")
    exit()

print("Switching parsers...")
print("Using WFST...")
sentence = input("Enter a sentence now:\n").lower().split()
wfst = init_wfst(sentence, grammar2)
display(wfst, sentence)
print("Showing full grid...")
wfst1 = complete_wfst(wfst, sentence, grammar2)
display(wfst1, sentence)

response = input("Should we try a different parser?\n")
if response.lower() != "yes":
    print("Finished.")
    exit()
# Works fine as well. Will look more into it later.

print("Switching parsers...")
print("Using ShiftReduce...")
sr_parser = nltk.ShiftReduceParser(grammar2)
sentence = input("Enter a sentence now:\n").lower().split()
for tree in sr_parser.parse(sentence):
    print(tree)
# ShiftReduce seems to provide no output - addressed in the chapter.

response = input("Should we try a different parser?\n")
if response.lower() != "yes":
    print("Finished.")
    exit()

print("Switching parsers...")
print("Using RecursiveDescent...")
rd_parser = nltk.RecursiveDescentParser(grammar2)
sentence = input("Enter a sentence now:\n").lower().split()
for tree in rd_parser.parse(sentence):
    print(tree)
# Hmm. Seems to enter an endless loop wherever left-recursion is ivolved, as predicted.

print("Finished.")