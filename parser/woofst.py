"""
This is the custom python module with all the functions needed in the scripts.
"""
import nltk
import re
import pandas as pd

### IMPORT ###
def load(text_path, gram_path, rule_path=None):
    print("\nLoading everything in:")
    # Load in the text via specified path.
    print("\nAccessing text...")
    try:
        text = open(text_path + ".txt", 'r')
        print("Done. Using " + text_path + ".txt as the chosen text.")
    # If the specified file cannot be found, throw an error and quit.
    except:
        print("Error. Text not found. Please check the spelling and the order of arguments.")
        exit()
    # Do the same for the grammar.
    print("\nAccessing grammar...")
    try:
        grammar = nltk.data.load(gram_path + ".cfg")
        print("Done. Using " + gram_path + ".cfg as the chosen grammar.")
        response = input("Would you like to see the grammar's productions? (yes/no)\n")
        if response == "yes":
            print("Listing the grammar's productions:")
            for p in grammar.productions():
                print(p)
        else:
            print("Understood. Moving on.")
    except:
        print("Error. Grammar not found. Please check the spelling and the order of arguments.")
        exit()
    if rule_path:
        # And the ruleset.
        print("\nAccessing terminal ruleset...")
        try:
            rules = open(rule_path + ".txt", 'r')
            print("Done. Using " + rule_path + ".txt as the chosen ruleset.")
        except:
            print("Error. Ruleset not found. Please check the spelling and the order of arguments.")
            exit()
    print("\nEverything loaded in fine.")


### TEXT ###
# Takes regex patterns and replaces them with spaces within a given text.
def replace(text, pattern):
    # Set up all the necessary variables
    alte_datei = open(text+'.txt','r')
    neue_datei = open(text+'_proc.txt','w')
    total_len = 0
    num_of_sents = 0
    sents = []
    # Remove symbols line-by-line, calculate the mean length.
    for line in alte_datei:
        new_line = re.sub(pattern, '', line)
        sentlist = new_line.split()
        total_len += len(sentlist)
        num_of_sents += 1
        sents.append(new_line)
    meanie = total_len/num_of_sents
    print("Mean length of sentence: " + str(meanie))
    # Use mean length as upper limit on what to write out.
    limit = int(meanie + 1)
    print("Writing only the sentences of length up to " + str(limit))
    for line in sents:
        anotherlist = line.split()
        if len(anotherlist) <= limit:
                neue_datei.write(line)
        else:
            continue
    neue_datei.close()

### GRAMMAR ###    
# Exploratory function that lists all the tags that occur in a given text. 
# Used to modify the list of terminals down the road.
def existing_classes(file):    
    #textfile = open(file + ".txt","r")
    collect_class = []
    for x in file:
        collect_class.append(x[0:x.find(" ")])
    return set(collect_class)
    
# Transforms the format of the terminals, combines them with nonterminal rules into a single context free grammar.
def make_gram(text, gram, classes):   
    st_cl = classes
    textfile = open(text + ".txt","r")
    collect_classes = []
    stated_classes_container = [[x[0],[]] for x in st_cl]
    
    # sammelt fuer jede class alle begriff ein
    for tf in textfile:
        for st,stc in zip(st_cl,stated_classes_container):
            if tf[0:tf.find(" ")] in st[1]:
                stc[1].append(tf[tf.find("'")+1:-2])
    
    # erstellt die einzelnen terminal-zeilen
    for stc in stated_classes_container:
        stc.insert(1, " ->")
    
    # kopiert die nonterminal-zeilen in eine neue grammatik
    fullgram = open(text + "_gram.cfg","w")
    for rule in open(gram + ".cfg", "r"):
        fullgram.write(rule)
    
    for w in stated_classes_container:
        fullgram.write(w[0]) # schreibt die Klasse
        fullgram.write(w[1]) # schreibt den pfeil "->"
        strich = 'n'        # wenn erstes element der Vokabelliste dann keinen "|"
        for z in w[2]:
            if len(w[2]) == 1:
                fullgram.write(str(" \""+z+"\"\n"))
            else:
                if strich == 'n':
                    fullgram.write(str(" \""+z+"\""))
                if strich == "j":
                    # Changed this a bit since the previous order would write every last member of a category twice.
                    if z == w[2][-1]:   # wenn letztes element der vokabelliste mache linebreak
                        fullgram.write(str(" | \""+z+"\"\n"))
                    else:
                        fullgram.write(str(" | \""+z+"\""))
                strich = "j"
    fullgram.close()
    
### PARSING ###
def parseit(text, gram, results):
    # Set up the lists that will serve as our table's columns.
    sentlist = []
    succlist = []
    parselist = []
    # Set up a variable to track the number of successful parses.
    successes = 0

    # Take sentences from text line-by-line, get parsing.
    grammar = nltk.data.load(gram + ".cfg")
    c_parser = nltk.ChartParser(grammar, trace=2)
    textfile = open(text + ".txt", 'r')
    for sentence in textfile:
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
        print("\n##################################################################\n")

    # Use the variable to calculate the percentage of successful parses.
    percent = int((successes / len(succlist))*100)
    print("Successfully parsed " + 
          str(successes) + 
          " sentences out of " + 
          str(len(succlist)) + 
          "(approximately " + str(percent) + "%).")
    
    print("\nWriting the detailed log to " + results + ".csv...")
    data = {"sent":sentlist, "success":succlist, "parses":parselist} # Sets up a dictionary based on the filled-out lists.
    df = pd.DataFrame.from_dict(data) # Turns it into a simple data frame.
    df.to_csv(results + ".csv", header=False, index=False) # Writes a file with the data frame.
    print("Done.")