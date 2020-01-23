def ersetzen(was,datei):

    import re
        
    alte_datei = open(datei+'.txt','r')
    neue_datei = open(datei+'_bearbeitet.txt','w')
    
    for line in alte_datei:
        new_line = re.sub(was, '', line)
        neue_datei.write(new_line)
    
    neue_datei.close()

zeichen_zum_ersetzen = r"( \.|,|``|\'\'|!|;|\?)"

ersetzen(zeichen_zum_ersetzen , 'text')

