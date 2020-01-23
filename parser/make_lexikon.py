
# zeigt alle in einer Datei vorkommenden Klassen an 
def existing_classes(datei):    
    textfile = open(datei+".txt","r")
    collect_class = []
    for x in textfile:
        collect_class.append(x[0:x.find(" ")])
    return set(collect_class)

# welche klassen gibt es?
existing_classes("rules")

# eine liste mit allen klassen:
stated_classes = [['.',['.']],['A',['ADJ']],
                  ['AD',['ADV']],['C',['CONJ']],
                  ['D',['DET']],['N',['NOUN']],
                  ['NU',['NUM']],['P',['PRON']],
                  ['PR',['PRT']],['V',['VERB']]]
                  
                
# Beispiel: ['V'              ['VERB','ADV']]
#             stated class    contains


def make_lexikon(datei):
    
    st_cl = stated_classes
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
    lexikon = open(datei+"_lexikon.txt","w")
    
    for w in stated_classes_container:
        lexikon.write(w[0]) # schreibt die Klasse
        lexikon.write(w[1]) # schreibt den pfeil "->"
        strich = 'n'        # wenn erstes element der Vokabelliste dann keinen "|"
        for z in w[2]:
            if strich == 'n':
                lexikon.write(str(" \""+z+"\""))
            if strich == "j":
                lexikon.write(str(" | \""+z+"\""))
            if z == w[2][-1]:   # wenn letztes element der vokabelliste mache linebreak
                lexikon.write(str(" | \""+z+"\"\n"))
            strich = "j"
    lexikon.close
    
# erstellt lexikon mit dem dateinamen + endung "_lexikon.txt"    
make_lexikon('rules') 


## 

stated_classes = [['.',['.']],['A',['ADJ']],
                  ['AD',['ADV']],['C',['CONJ']],
                  ['D',['DET']],['N',['NOUN']],
                  ['NU',['NUM']],['P',['PRON']],
                  ['PR',['PRT']],['V',['VERB']]]
                  
                
# alles was kein 0 bis 9 und a bis z gross klein ist 

sentence = re.sub(' . ', '', line).strip()
sentence = re.sub(' , ', '', line).strip()
sentecee

sentence = re.sub()
            