import nltk
import sys
import re
import pandas as pd
### ANACONDA PROMPT CODE: "python <scriptname> <firstargument> <secondargument> <thirdargument>"

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt")###
gram_path = sys.argv[1] # Prepared grammar file name, e.g. simple_gram.cfg
text_path = sys.argv[2] # Prepared text file name, e.g. simple_text.txt
results_path = sys.argv[3] # Arbitrarily named .csv that the script generates and saves the table into, e.g. results.csv

### Greet the user ###
print("\n####################################################")
print("Hello. This is a basic script for parsing sentences.")
print("####################################################")

### Load everything in ###
# Load in the grammar via specified path.
print("\nAccessing grammar...")
try:
    grammar = nltk.data.load(gram_path)
    c_parser = nltk.ChartParser(grammar, trace=2)
    print("Done. Using " + gram_path + " as the chosen grammar.\n\nListing the grammar's productions:")
    for p in grammar.productions():
        print(p)
# If the specified file cannot be found, throw an error and quit.
except:
    print("\nError. Grammar not found. Please check the spelling and the order of arguments.")
    exit()
# Do the same for the text.
print("\nAccessing text...")
try:
    text = open(text_path, 'r')
    print("Done. Using " + text_path + " as the chosen text.")
except:
    print("\nError. Text not found. Please check the spelling and the order of arguments.")
    exit()

### Prompt to start the parsing process ###
response = input("\nEverything loaded in fine. Shall we try and parse the bitch? (yes/no)\n")
if response.lower().strip() != "yes":
    print("Okay. Be that way.")
    exit()
else:
    print("\nUsing Chart as the chosen parser.")

### Core loop ###
# Set up the lists that will serve as our table's columns.
sentlist = []
succlist = []
parselist = []
# Set up a variable to track the number of successful parses.
successes = 0

# Take sentences from text line-by-line, get parsing.
for sentence in text:
    with open('debuggin.txt', 'w') as file:
        file.write(sentence)
    parses = [] # Save all possible trees to a list
    for parse in c_parser.parse(sentence.lower().split()):
        parses.append(str(parse))
    parseset = [] # Throw this list into another just in case there are multiple trees.
    for tree in parses:
        parseset.append(str(tree))
        
    # Clean up and start building rows for the dataframe.
    sentlist.append(sentence)
    parselist.append("\n".join(parseset))
    if len(parses) == 0:
        succlist.append(0)
    else:
        succlist.append(1)
        successes += 1

# Use the variable to calculate the percentage of successful parses.
    percent = int((successes / len(succlist))*100)
    print("Successfully parsed " + 
          str(successes) + 
          " sentences out of " + 
          str(len(succlist)) + 
          "(approximately " + str(percent) + "%).")
    print("Writing the detailed log to " + results_path + "...")

### Building and saving a Dataframe ###
# IMPORTANT: Length of all three arrays should be identical, as they correspond to the columns of the dataframe. 
# This is why for multiple trees per sent, we throw them in a list of their own and append that instead.
data = {"sent":sentlist, "success":succlist, "parses":parselist} # Sets up a dictionary based on the filled-out lists.
df = pd.DataFrame.from_dict(data) # Turns it into a simple data frame.
df.to_csv(results_path, header=False, index=False)
print("Done.")

response = input("\nTo quit the program, press ENTER.\n")
if response == "":
    exit()