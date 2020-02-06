import woofst as wf
import sys

### CHANGE THESE TO CUSTOM PATHS IF RUNNING CODE IN SPYDER (e.g. "C:\Users\User\Desktop\filename.txt")###
try:
    text_path = sys.argv[1] # Prepared text file name
    gram_path = sys.argv[2] # Prepared grammar file name
    rule_path = sys.argv[3] # Prepared rules file name
except:
    text_path = "text"
    gram_path = "overhead"
    rule_path = "rules"

### Greet the user ###
print("\n########################################################################################")
print("Hello. This is the script for processing the selected text and producing a full grammar.")
print("########################################################################################")

### Check that all specified files exist ###
wf.load(text_path, gram_path, rule_path)

### Prompt to start processing ###
response = input("Ready to process? (yes/no)\n")
if response.lower().strip() != "yes":
    print("Okay. Be that way.")
    exit()
else:
    print("\nModifying " + text_path + ".txt and saving it to new file...")
   
### Use this regex to modify text ###   
zeichen_zum_ersetzen = r"( \.|,|``|\'\'|!|;|\?)"
wf.replace(text_path, zeichen_zum_ersetzen)
print("Done.")

### Run a function to see which tags are in the text ###
rules = open(rule_path + ".txt", 'r')
response = input("\nWould you like to see the ruleset's POS tags? (yes/no)\n")
if response == "yes":
    print("The chosen ruleset features the following POS tags:")
    for tag in sorted(wf.existing_classes(rules)):
        print(tag)
else:
    print("Understood. Moving on.")
    
### Use the info to possibly update this list ###
# See https://en.wikipedia.org/wiki/Brown_Corpus for info on the tags.
stated_classes = [
                ['DOT',['.','(',')','--',',',':',',-HL']],
                ['A',['JJ','JJR','JJS','JJT','JJ-TL','VBN']],
                ['Adv',['ABL','NR','NRS','QL','QLP','RB','RBR','RBT','RN','RP']],
                ['C',['CC','CS','CC-TL','BED','BEDZ','BEM','BEN','BER','BEZ','BBB','DO','DOD','DOZ','HV','HVD','HVN','HVZ','MD','BEZ*','DO*','MD*']],
                ['D',['AP','AT','DT','DTI','DTS','DTX','WDT']],
                ['DP',['NP','NPS','PN','PPL','PPLS','PPO','PPS','PPSS','NP-TL']],
                ['DPPOS',['NN$','NNS$','NP$','NPS$','PN$','PP$','PP$$','NN$-TL']],
                ['N',['NN','NNS','NN-TL','NNS-TL']],
                ['NEG',['*']],
                ['P',['IN']],
                ['Q',['ABN','ABX','CD','OD']],
                ['QS',['WP$','WPO','WPS','WQL','WRB']],
                ['V',['BE','BED','BEDZ','BEG','BEM','BEN','BER','BEZ','BBB','DO','DOD','DOZ','HV','HVD','HVG','HVN','HVZ','MD','VB','VBD','VBG','VBP','VBZ','BEZ*','DO*','MD*']],
                ['EX',['EX']],
                ['TRASH',['-TL','-NC','-*','TO','FW-','UH','DT+BEZ']]
                ]


print("\nCombining the nonterminal grammar with the modified ruleset and saving to new file...")
wf.make_gram(rule_path, gram_path, stated_classes)
print("Done.")

# Exit the program.
response = input("\nTo quit the program, press ENTER.\n")
if response == "":
    exit()