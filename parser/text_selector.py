from nltk.corpus import brown
import sys
### ANACONDA PROMPT CODE: "python <scriptname> <firstargument> <secondargument>"

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt")###
path1 = sys.argv[1] # Raw text file name, e.g. raw.txt
path2 = sys.argv[2] # Tagged text file name, e.g. tagged.txt

print("Welcome to text selector.\nThe Brown corpus has texts from the following genres:")
for cat in brown.categories():
    print(cat)

### ACCESSING IDS ###
catquery = input("\nPlease enter a genre to see the list of its files:\n")
flag = "I am a flag."
while flag:
    if catquery.lower().strip() not in brown.categories():
        catquery = input("\nError. Please spell the genre correctly:\n")
    else:
        print("\nGenre accepted. Retrieving file IDs:")
        flag = ""
for fileid in brown.fileids(categories=[catquery]):
    print(fileid)


### ACCESSING AND SAVING TEXTS ###
idquery = input("\nPlease select an ID to access text:\n")
flag = "I am a flag."
while flag:
    if idquery.lower().strip() not in brown.fileids(categories=[catquery]):
        idquery = input("\nError. Please spell the ID correctly:\n")
    else:
        print("\nID accepted.\nRetrieving raw text and saving as " + str(path1) + "...")
        text_raw = brown.raw(fileids=[idquery])
        with open(path1, "w") as file_raw:
            print(text_raw, file=file_raw)
            print("Done.")
        print("\nRetrieving all items from the tagged text and saving as " + str(path2) + "...")
        text_tagged = brown.tagged_words(fileids=[idquery], tagset='universal')
        new_tagged = []
        with open(path2, "w") as file_tagged:
            for word, tag in set(text_tagged):
                new_tagged.append((tag,word))
            for tagset in sorted(new_tagged):
                print(tagset, file=file_tagged)
            print("Done.")
        flag = ""

response = input("\nTo quit the selector, press ENTER.\n")
if not response:
    exit()