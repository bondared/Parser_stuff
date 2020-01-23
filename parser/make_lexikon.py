import sys
# Added to make the script a little more flexible.
try:
    path = sys.argv[1] # Allows a custom filename.
    path2 = sys.argv[2] # 
except:
    path = "rules"     # Uses "rules" as the default.
    path2 = "overhead"


# zeigt alle in einer Datei vorkommenden Klassen an 
def existing_classes(datei):    
    textfile = open(datei+".txt","r")
    collect_class = []
    for x in textfile:
        collect_class.append(x[0:x.find(" ")])
    return set(collect_class)

# welche klassen gibt es?
print(existing_classes(path))

# eine liste mit allen klassen:
# Von https://en.wikipedia.org/wiki/Brown_Corpus genommen, mit den im Text vorkommenden Tags verglichen.
# Es bleiben noch mehrere unsichere Stellen - die unsichersten Kategorien sind unter TRASH gepackt
# Alle anderen Kategorien müssen auch besprochen werden - wo der jeweilige Tag hingehört, hängt von unserem syntaktischen Wissen ab.
stated_classes = [
                ['DOT',['.','(',')','--',',',':',',-HL']],
                ['A',['JJ','JJR','JJS','JJT','JJ-HL','JJR-HL','JJ-TL']],
                ['Adv',['ABL','NR','NRS','QL','QLP','RB','RBR','RBT','RN','RP']],
                ['C',['CC','CS','CC-TL']],
                ['D',['AP','AT','DT','DTI','DTS','DTX','AT-HL']],
                ['DP',['NP','NPS','PN','PPL','PPLS','PPO','PPS','PPSS','NP-TL']],
                ['DPPOS',['NN$','NNS$','NP$','NPS$','PN$','PP$','PP$$','NN$-TL']],
                ['N',['NN','NNS','NN-TL','NNS-HL','NNS-TL','NN-HL']],
                ['NEG',['*']],
                ['P',['IN']],
                ['Q',['ABN','ABX','CD','OD']],
                ['V',['BE','BED','BEDZ','BEG','BEM','BEN','BER','BEZ','BBB','DO','DOD','DOZ','HV','HVD','HVG','HVN','HVZ','MD','VB','VBD','VBG','VBN','VBP','VBZ','VBN-HL','VBG-HL']],
                # Die mit Bindestrichen verwiesene Kategorien können an jedes Wort beliebig angehängt werden.
                # Wir müssen also einen Weg finden, damit auch diese ihren jeweiligen Kategorien halbwegs automatisch zugewiesen werden.
                ['TRASH',['-HL','-TL','-NC','TO','-*','EX','FW-','UH','WDT','WP$','WPO','WPS','WQL','WRB','DT+BEZ','BEZ*','DO*','MD*']]
                ]
                  
                
# Beispiel: ['V'              ['VERB','ADV']]
#             stated class    contains

def make_lexikon(datei, grammatik, classes):   
# Added "classes" as an argument so that the function is not as tied to a predefined variable.
    st_cl = classes
    textfile = open(datei+".txt","r")
    collect_classes = []
    stated_classes_container = [[x[0],[]] for x in st_cl]
    
    # sammelt fuer jede class alle begriff ein
    for tf in textfile:
        for st,stc in zip(st_cl,stated_classes_container):
            if tf[0:tf.find(" ")] in st[1]:
                stc[1].append(tf[tf.find("'")+1:-2])
    
    # erstellt die einzelnen lexikon zeilen
    for stc in stated_classes_container:
        stc.insert(1, " ->")
    
    
    lexikon = open(datei + "_gram.cfg","w")
    for rule in open(grammatik + ".cfg", "r"):
        lexikon.write(rule)
    
    for w in stated_classes_container:
        lexikon.write(w[0]) # schreibt die Klasse
        lexikon.write(w[1]) # schreibt den pfeil "->"
        strich = 'n'        # wenn erstes element der Vokabelliste dann keinen "|"
        for z in w[2]:
            if len(w[2]) == 1:
                lexikon.write(str(" \""+z+"\"\n"))
            else:
                if strich == 'n':
                    lexikon.write(str(" \""+z+"\""))
                if strich == "j":
                    # Changed this a bit since the previous order would write every last member of a category twice.
                    if z == w[2][-1]:   # wenn letztes element der vokabelliste mache linebreak
                        lexikon.write(str(" | \""+z+"\"\n"))
                    else:
                        lexikon.write(str(" | \""+z+"\""))
                strich = "j"
    lexikon.close()
    
# erstellt lexikon mit dem dateinamen + endung "_lexikon.txt"    
make_lexikon(path, path2, stated_classes)