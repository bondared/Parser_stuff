def ersetzen(was,durch_was,datei):

    import re
        
    alte_datei = open(datei+'.txt','r')
    neue_datei = open(datei+'1.txt','w')
    
    for line in alte_datei:
        new_line = re.sub(was, durch_was, line)
        neue_datei.write(new_line)
    
    neue_datei.close()
        
  


ersetzen(' \.'  ,'',  'text'     )
ersetzen(','    ,'',  'text1'    )
ersetzen('``'   ,'',  'text11'   )
ersetzen('\'\'' ,'',  'text111'  )
ersetzen('!'    ,'',  'text1111' )
ersetzen(';'    ,'',  'text11111')
