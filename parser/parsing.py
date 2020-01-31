import woofst as wf
import sys

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt")###
try:
    text_path = sys.argv[1] # Prepared text file name, e.g. simple_text
    gram_path = sys.argv[2] # Prepared grammar file name, e.g. simple_gram
    res_path = sys.argv[3] # .csv table file name, e.g. results
except:
    text_path = "text_proc"
    gram_path = "rules_gram"
    res_path = "results"

### Greet the user ###
print("\n####################################################")
print("Hello. This is the script for parsing sentences.")
print("####################################################")

### Check that all specified files exist ###
wf.load(text_path, gram_path)

### Prompt to start the parsing process ###
response = input("Shall we try and parse the bitch? (yes/no)\n")
if response.lower().strip() != "yes":
    print("Okay. Be that way.")
    exit()
else:
    print("\nUsing Chart as the chosen parser.")
    wf.parseit(text_path, gram_path, res_path)

# Exit the program.
response = input("\nTo quit the program, press ENTER.\n")
if response == "":
    exit()