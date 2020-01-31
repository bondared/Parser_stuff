import sys
from nltk.corpus import brown

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt").###
try:
    path1 = sys.argv[1] # Raw text file name, e.g. text.
    path2 = sys.argv[2] # Preliminary rules file name, e.g. rules.
except:
    path1 = "text"
    path2 = "rules"

### Greet the user ###
print("\n#####################################################################")
print("Hello. This is the script for selecting texts and extracting POS tags.")
print("######################################################################")
print("\nThe Brown corpus has texts from the following genres:")
for cat in brown.categories():
    print(cat)

### ACCESSING IDS ###
catquery = input("\nPlease enter a genre to see the list of its files:\n")
flag = "I am a flag."
while flag:
    # Make sure entered category is in the corpus.
    if catquery.lower().strip() not in brown.categories():
        catquery = input("\nError. Please spell the genre correctly:\n")
    else:
        print("\nGenre accepted. Retrieving file IDs:")
        flag = ""
# Use the category to subset the corpus and access the IDs associated with it.
for fileid in brown.fileids(categories=[catquery]):
    print(fileid)


### ACCESSING AND SAVING TEXTS AND RULES ###
idquery = input("\nPlease select an ID to access text:\n")
flag = "I am a flag."
while flag:
    # Make sure entered ID is in the selected category. If not, ask to enter an ID within the chosen category.
    if idquery.lower().strip() not in brown.fileids(categories=[catquery]):
        idquery = input("\nError. Please spell the ID correctly:\n")
    else:
        print("\nID accepted.\nRetrieving raw text and saving as " + str(path1) + "...")
        
        # Import a list of lists from Brown. Every sentence is a list of strings.
        raw_sents = brown.sents(fileids=[idquery])
        clean_sents = []
        for sent in raw_sents:
            # Go into the list of sents, make every sent a single string.
            clean_sent = " ".join(sent)
            clean_sents.append(clean_sent)
        # Make the whole text into a single string. We're basically undoing most of the preprocesing work.
        clean_text = "\n".join(clean_sents)
        # Save it to the first argument path.
        with open(path1 + ".txt", "w") as mr_clean:
            print(clean_text, file = mr_clean)
            print("Done.")
        
        print("\nRetrieving all terminals from the tagged text and saving as " + str(path2) + ".txt...")
        # Import the list of tuples from Brown. Every tuple is ("Word", "Tag").
        text_tagged = brown.tagged_words(fileids=[idquery])
        ruleset = []
        with open(path2 + ".txt", "w") as file_tagged:
            # Reduce the list of tuples to contain only unique items.
            for word, tag in text_tagged:
                # Rewrite the tuples to the form "Tag" -> "Word", throw them into a new list.
                # NB: Make each word lowercase so that we wouldn't have duplicated entries in the ruleset.
                rule = str(tag) + " -> '" + str(word.lower()) + "'"
                ruleset.append(rule)
            # Write every element from the new list one-by-one to the second argument path.  
            for rule in sorted(set(ruleset)):
                print(rule, file=file_tagged)
            print("Done.")
        flag = ""

# Just needed something to bugtest.
response = input("\nTo quit the selector, press ENTER.\n")
if not response:
    exit()