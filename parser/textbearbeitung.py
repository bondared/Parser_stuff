import sys
try:
    path1 = sys.argv[1]
except:
    path1 = "text"

def ersetzen(was,datei):

    import re
        
    alte_datei = open(datei+'.txt','r')
    neue_datei = open(datei+'_bearbeitet.txt','w')
    
    for line in alte_datei:
        new_line = re.sub(was, '', line)
        neue_datei.write(new_line.strip())
    
    neue_datei.close()

zeichen_zum_ersetzen = r"( \.|,|``|\'\'|!|;|\?)"

ersetzen(zeichen_zum_ersetzen , path1)
