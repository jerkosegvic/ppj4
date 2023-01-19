lines = []
globalne_varijable = []
labela = 0
naso_f = False

def broj_labele():
    global labela
    labela += 1
    return 'L' + str(labela)

def upisi(kod):
  global lines 

  global naso_f
  if kod.startswith('F_') and not naso_f:
      naso_f = True
      lines.extend(["    CALL F_main", "    HALT"])
  
  kod = [kod]
  lines.extend(kod)

def upisi_varijablu(varijabla, vrijednost):

    if vrijednost == None:
        vrijednost = 0
    i = int(vrijednost)
    globalne_varijable.append("VAR_" + varijabla + " DW " + format(i, 'X'))

def upisi_niz(niz_ime, velicina,vrijednosti):
    rv = "VAR_" + niz_ime 

    for i in range(velicina):
        ubac = 0
        if vrijednosti != None and i < len(vrijednosti):
            ubac = int(vrijednosti[i])
        rv += "    DW " + format(ubac, 'X') + "\n"
    globalne_varijable.append(rv)

def zavrsi():
  with open('a.frisc', 'w') as file:

    global lines
    global globalne_varijable
    
    finalni_kod = '\n'.join(lines)
    glob_var = '\n'.join(globalne_varijable)

    file.writelines(["    MOVE 40000, R7\n"])
    file.writelines(finalni_kod)
    file.writelines(glob_var)
    file.write('\n')


if __name__ == '__main__':
  upisi('\thello')
  upisi('world\n!')
  zavrsi()